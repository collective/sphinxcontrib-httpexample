# -*- coding: utf-8 -*-
from ast import unparse
from io import StringIO
from shlex import quote as shlex_quote
from sphinxcontrib.httpexample.utils import is_json
from sphinxcontrib.httpexample.utils import maybe_str
from urllib.parse import parse_qs
from urllib.parse import urlparse
import ast
import json
import re
import string


_find_unsafe = re.compile(
    r"[^\w@%+=:,./-" + string.ascii_letters + string.digits + "]",
).search


def shlex_double_quote(s):
    """Return a shell-escaped version of the string *s*."""
    if not s:
        return '""'
    if _find_unsafe(s) is None:
        return s

    # use double quotes, and put double quotes into single quotes
    # the string $"b is then quoted as "$"'"'"b"
    return re.sub(r'^""|""$', "", ('"' + s.replace('"', '"\'"\'"') + '"'))


EXCLUDE_HEADERS = [
    "Authorization",
    "Host",
]
EXCLUDE_HEADERS_HTTP = EXCLUDE_HEADERS + []
EXCLUDE_HEADERS_REQUESTS = EXCLUDE_HEADERS + []


def build_curl_command(request):
    parts = ["curl", "-i"]

    # Method
    parts.append("-X {}".format(request.command))

    # URL
    parts.append(shlex_quote(request.url()))

    # Authorization (prepare)
    method, token = request.auth()

    # Headers
    for header in sorted(request.headers):
        if header in EXCLUDE_HEADERS:
            continue
        header_line = shlex_double_quote(
            "{}: {}".format(header, request.headers[header]),
        )
        parts.append("-H {}".format(header_line))

    if method != "Basic" and "Authorization" in request.headers:
        header = "Authorization"
        header_line = shlex_double_quote(
            "{}: {}".format(header, request.headers[header]),
        )
        parts.append("-H {}".format(header_line))

    # JSON
    data = maybe_str(request.data())
    if data:
        if is_json(request.headers.get("Content-Type", "")):
            data = json.dumps(data)
        parts.append("--data-raw '{}'".format(data))

    # Authorization
    if method == "Basic":
        parts.append("--user {}".format(token))

    return " ".join(parts)


def build_wget_command(request):
    parts = ["wget", "-S", "-O-"]

    # Method
    if request.command not in ["GET", "POST"]:
        parts.append("--method={}".format(request.command))

    # URL
    parts.append(shlex_quote(request.url()))

    # Authorization (prepare)
    method, token = request.auth()

    # Headers
    for header in sorted(request.headers):
        if header in EXCLUDE_HEADERS:
            continue
        header_line = shlex_double_quote(
            "{}: {}".format(header, request.headers[header]),
        )
        parts.append("--header={}".format(header_line))

    if method != "Basic" and "Authorization" in request.headers:
        header = "Authorization"
        header_line = shlex_double_quote(
            "{}: {}".format(header, request.headers[header])
        )
        parts.append("--header={}".format(header_line))

    # JSON or raw data
    data = maybe_str(request.data())
    if data:
        if is_json(request.headers.get("Content-Type", "")):
            data = json.dumps(data)
        if request.command == "POST":
            parts.append("--post-data='{}'".format(data))
        elif request.command != "POST":
            parts.append("--body-data='{}'".format(data))

    # Authorization
    if method == "Basic":
        user, password = token.split(":")
        parts.append("--auth-no-challenge")
        parts.append("--user={}".format(user))
        parts.append("--password={}".format(password))

    return " ".join(parts)


def build_httpie_command(request):
    parts = ["http"]
    redir_input = ""

    # Method
    if request.command != "GET":
        parts.append(request.command)

    # URL
    parts.append(shlex_quote(request.url()))

    # Authorization (prepare)
    method, token = request.auth()

    # Headers
    for header in sorted(request.headers):
        if header in EXCLUDE_HEADERS_HTTP:
            continue
        parts.append(
            "{}:{}".format(
                header,
                shlex_double_quote(request.headers[header]),
            )
        )

    if method != "Basic" and "Authorization" in request.headers:
        header = "Authorization"
        parts.append(
            "{}:{}".format(
                header,
                shlex_double_quote(request.headers[header]),
            )
        )

    # JSON or raw data
    data = maybe_str(request.data())
    if data:

        if is_json(request.headers.get("Content-Type", "")):
            # We need to explicitly set the separators to get consistent
            # whitespace handling across Python 2 and 3. See
            # https://bugs.python.org/issue16333 for details.
            redir_input = shlex_quote(
                json.dumps(data, indent=2, sort_keys=True, separators=(",", ": "))
            )
        else:
            redir_input = shlex_quote(data)

    # Authorization
    if method == "Basic":
        parts.append("-a {}".format(token))

    cmd = " ".join(parts)

    if not redir_input:
        return cmd

    else:
        return "echo {} | {}".format(redir_input, cmd)


def flatten_parsed_qs(data):
    """Flatten single value lists in parse_qs results."""
    for key, value in data.items():
        if isinstance(value, list) and len(value) == 1:
            data[key] = value[0]
    return data


def build_requests_command(request):
    # Method
    tree = ast.parse("requests.{}()".format(request.command.lower()))
    call = tree.body[0].value
    call.keywords = []

    # URL
    call.args.append(ast.Constant(request.url()))

    # Authorization (prepare)
    method, token = request.auth()

    # Headers
    header_keys = []
    header_values = []
    for header in sorted(request.headers):
        if header in EXCLUDE_HEADERS_REQUESTS:
            continue
        header_keys.append(ast.Constant(header))
        header_values.append(ast.Constant(request.headers[header]))
    if method != "Basic" and "Authorization" in request.headers:
        header_keys.append(ast.Constant("Authorization"))
        header_values.append(ast.Constant(request.headers["Authorization"]))
    if header_keys and header_values:
        call.keywords.append(
            ast.keyword("headers", ast.Dict(header_keys, header_values))
        )

    # JSON or raw data
    data = maybe_str(request.data())

    # Form data
    content_type = request.headers.get("Content-Type")
    if content_type == "application/x-www-form-urlencoded":
        if not isinstance(data, dict):
            data = flatten_parsed_qs(parse_qs(data))

    def astify_json_obj(obj):
        obj = maybe_str(obj)
        if isinstance(obj, str):
            return ast.Constant(obj)
        elif isinstance(obj, bool):
            return ast.Name(str(obj), ast.Load())
        elif isinstance(obj, int):
            return ast.Name(str(obj), ast.Load())
        elif isinstance(obj, float):
            return ast.Name(str(obj), ast.Load())
        elif isinstance(obj, list):
            json_values = []
            for v in obj:
                json_values.append(astify_json_obj(v))
            return ast.List(json_values, ast.Load())
        elif isinstance(obj, dict):
            json_values = []
            json_keys = []
            for k, v in obj.items():
                json_keys.append(ast.Constant(maybe_str(k)))
                json_values.append(astify_json_obj(v))
            return ast.Dict(json_keys, json_values)
        else:
            raise Exception("Cannot astify {0:s}".format(str(obj)))

    if data:
        if is_json(request.headers.get("Content-Type", "")):
            call.keywords.append(ast.keyword("json", astify_json_obj(data)))
        else:
            call.keywords.append(ast.keyword("data", ast.Constant(data)))

    # Authorization
    if method == "Basic":
        token = maybe_str(token)
        call.keywords.append(
            ast.keyword(
                "auth", ast.Tuple(tuple(map(ast.Constant, token.split(":"))), None)
            )
        )

    return unparse(tree).strip()


def build_urllib3_command(request):
    # Imports
    imports = [
        ast.Import(names=[ast.alias(name="urllib3")]),
    ]
    content_type = request.headers.get("Content-Type", "")
    if is_json(content_type):
        imports.append(ast.Import(names=[ast.alias(name="json")]))
    elif content_type == "application/x-www-form-urlencoded":
        imports.append(
            ast.ImportFrom(
                module="urllib.parse",
                names=[ast.alias(name="urlencode")],
                level=0,
            )
        )

    # Method
    tree = ast.parse("http.request()")
    call = tree.body[0].value
    call.keywords = []

    # Method
    call.args.append(ast.Constant(request.command))

    # URL
    call.args.append(ast.Constant(request.url()))

    # Authorization (prepare)
    method, token = request.auth()
    if method == "Basic":
        imports.append(
            ast.ImportFrom(
                module="urllib3.util",
                names=[ast.alias(name="make_headers")],
                level=0,
            )
        )

    # Headers
    headers = {}
    for header in sorted(request.headers):
        if header in EXCLUDE_HEADERS_REQUESTS:
            continue
        headers[header] = request.headers[header]

    if method != "Basic" and "Authorization" in request.headers:
        headers["Authorization"] = request.headers["Authorization"]

    header_keys = [ast.Constant(k) for k in headers.keys()]
    header_values = [ast.Constant(v) for v in headers.values()]
    headers_dict = ast.Dict(header_keys, header_values)

    if method == "Basic":
        token = maybe_str(token)
        headers_assignment = ast.Assign(
            targets=[ast.Name(id="headers", ctx=ast.Store())],
            value=headers_dict,
        )
        auth_headers = ast.Call(
            func=ast.Name(id="make_headers", ctx=ast.Load()),
            args=[],
            keywords=[
                ast.keyword(
                    "basic_auth",
                    ast.Constant(token),
                )
            ],
        )
        update_call = ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="headers", ctx=ast.Load()),
                    attr="update",
                    ctx=ast.Load(),
                ),
                args=[auth_headers],
                keywords=[],
            )
        )
        call.keywords.append(
            ast.keyword(arg="headers", value=ast.Name(id="headers", ctx=ast.Load()))
        )
    elif headers:
        call.keywords.append(ast.keyword(arg="headers", value=headers_dict))

    # JSON or raw data
    data = maybe_str(request.data())

    # Form data
    if content_type == "application/x-www-form-urlencoded":
        if not isinstance(data, dict):
            data = flatten_parsed_qs(parse_qs(data))

    def astify_json_obj(obj):
        obj = maybe_str(obj)
        if isinstance(obj, str):
            return ast.Constant(obj)
        elif isinstance(obj, bool):
            return ast.Name(str(obj), ast.Load())
        elif isinstance(obj, int):
            return ast.Name(str(obj), ast.Load())
        elif isinstance(obj, float):
            return ast.Name(str(obj), ast.Load())
        elif isinstance(obj, list):
            json_values = []
            for v in obj:
                json_values.append(astify_json_obj(v))
            return ast.List(json_values, ast.Load())
        elif isinstance(obj, dict):
            json_values = []
            json_keys = []
            for k, v in obj.items():
                json_keys.append(ast.Constant(maybe_str(k)))
                json_values.append(astify_json_obj(v))
            return ast.Dict(json_keys, json_values)
        else:
            raise Exception("Cannot astify {0:s}".format(str(obj)))

    if data:
        if is_json(content_type):
            call.keywords.append(
                ast.keyword(
                    "body",
                    ast.Call(
                        func=ast.Attribute(
                            value=ast.Call(
                                func=ast.Attribute(
                                    value=ast.Name(id="json", ctx=ast.Load()),
                                    attr="dumps",
                                    ctx=ast.Load(),
                                ),
                                args=[astify_json_obj(data)],
                                keywords=[],
                            ),
                            attr="encode",
                            ctx=ast.Load(),
                        ),
                        args=[ast.Constant("utf-8")],
                        keywords=[],
                    ),
                )
            )
        elif content_type == "application/x-www-form-urlencoded":
            call.keywords.append(
                ast.keyword(
                    "body",
                    ast.Call(
                        func=ast.Name(id="urlencode", ctx=ast.Load()),
                        args=[astify_json_obj(data)],
                        keywords=[],
                    ),
                )
            )
        else:
            call.keywords.append(ast.keyword("body", ast.Constant(data)))

    # Create a PoolManager
    pool_manager = ast.Assign(
        targets=[ast.Name(id="http", ctx=ast.Store())],
        value=ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="urllib3", ctx=ast.Load()),
                attr="PoolManager",
                ctx=ast.Load(),
            ),
            args=[],
            keywords=[],
        ),
    )

    # Response
    response = ast.Assign(targets=[ast.Name(id="r", ctx=ast.Store())], value=call)

    # The whole tree
    tree.body = imports + [pool_manager]
    if method == "Basic":
        tree.body.extend([headers_assignment, update_call])
    tree.body.append(response)

    ast.fix_missing_locations(tree)
    return unparse(tree).strip()

    # Method
    tree = ast.parse("http.request()")
    call = tree.body[0].value
    call.keywords = []

    # Method
    call.args.append(ast.Constant(request.command))

    # URL
    call.args.append(ast.Constant(request.url()))

    # Authorization (prepare)
    method, token = request.auth()
    if method == "Basic":
        imports.append(
            ast.ImportFrom(
                module="urllib3.util",
                names=[ast.alias(name="make_headers")],
                level=0,
            )
        )

    # Headers
    header_keys = []
    header_values = []
    # Use a dictionary to store headers to avoid duplicates
    headers = {}
    for header in sorted(request.headers):
        if header in EXCLUDE_HEADERS_REQUESTS:
            continue
        headers[header] = request.headers[header]

    if method != "Basic" and "Authorization" in request.headers:
        headers["Authorization"] = request.headers["Authorization"]

    if method == "Basic":
        token = maybe_str(token)
        # Create basic auth header
        auth_headers = ast.Call(
            func=ast.Name(id="make_headers", ctx=ast.Load()),
            args=[],
            keywords=[
                ast.keyword(
                    "basic_auth",
                    ast.Constant(token),
                )
            ],
        )
        # Merge with existing headers
        if headers:
            # Update the auth headers with the existing headers
            # headers.update(auth_headers)
            # Cannot do this easily with AST, so I'll just have two headers arguments
            # which is not ideal, but it's what the previous code was doing
            pass  # Will be handled later

    header_keys = [ast.Constant(k) for k in headers.keys()]
    header_values = [ast.Constant(v) for v in headers.values()]

    if header_keys and header_values:
        headers_dict = ast.Dict(header_keys, header_values)
        if method == "Basic":
            # merge headers
            headers_dict = ast.Call(
                func=ast.Attribute(
                    value=headers_dict,
                    attr="update",
                    ctx=ast.Load(),
                ),
                args=[
                    ast.Call(
                        func=ast.Name(id="make_headers", ctx=ast.Load()),
                        args=[],
                        keywords=[
                            ast.keyword(
                                "basic_auth",
                                ast.Constant(token),
                            )
                        ],
                    )
                ],
                keywords=[],
            )
            # The update call returns None, so we can't use it directly
            # I will create a temporary variable and then update it
            # temp_headers = {'a': 'b'}
            # temp_headers.update(make_headers(basic_auth='user:pass'))
            # r = http.request(..., headers=temp_headers)
            # This is getting too complex. I will generate the headers dict and then
            # add the auth to it if needed.

            # Rebuild headers dict
            headers_with_auth = ast.Dict(header_keys, header_values)
            call.keywords.append(ast.keyword(arg="headers", value=headers_with_auth))
            # It's tricky to merge dicts in AST.
            # A simple way is to have two keywords, but that's invalid for the call.
            # Another way is to create a new dict and merge them.
            # Let's try to do it properly.
            # 1. create the headers dict
            # 2. if basic auth, create auth dict
            # 3. merge them: {**headers, **auth} (python 3.5+)
            # The target is 3.10 so this is fine.
            final_headers = ast.Dict(header_keys, header_values)
            if method == "Basic":
                auth_header = ast.Call(
                    func=ast.Name(id="make_headers", ctx=ast.Load()),
                    args=[],
                    keywords=[
                        ast.keyword(
                            "basic_auth",
                            ast.Constant(token),
                        )
                    ],
                )
                final_headers = ast.Dict(
                    keys=[None, None], values=[final_headers, auth_header]
                )

            call.keywords.append(ast.keyword(arg="headers", value=final_headers))
        else:
            call.keywords.append(
                ast.keyword(arg="headers", value=ast.Dict(header_keys, header_values))
            )

    # JSON or raw data
    data = maybe_str(request.data())

    # Form data
    if content_type == "application/x-www-form-urlencoded":
        if not isinstance(data, dict):
            data = flatten_parsed_qs(parse_qs(data))

    def astify_json_obj(obj):
        obj = maybe_str(obj)
        if isinstance(obj, str):
            return ast.Constant(obj)
        elif isinstance(obj, bool):
            return ast.Name(str(obj), ast.Load())
        elif isinstance(obj, int):
            return ast.Name(str(obj), ast.Load())
        elif isinstance(obj, float):
            return ast.Name(str(obj), ast.Load())
        elif isinstance(obj, list):
            json_values = []
            for v in obj:
                json_values.append(astify_json_obj(v))
            return ast.List(json_values, ast.Load())
        elif isinstance(obj, dict):
            json_values = []
            json_keys = []
            for k, v in obj.items():
                json_keys.append(ast.Constant(maybe_str(k)))
                json_values.append(astify_json_obj(v))
            return ast.Dict(json_keys, json_values)
        else:
            raise Exception("Cannot astify {0:s}".format(str(obj)))

    if data:
        if is_json(content_type):
            call.keywords.append(
                ast.keyword(
                    "body",
                    ast.Call(
                        func=ast.Attribute(
                            value=ast.Call(
                                func=ast.Attribute(
                                    value=ast.Name(id="json", ctx=ast.Load()),
                                    attr="dumps",
                                    ctx=ast.Load(),
                                ),
                                args=[astify_json_obj(data)],
                                keywords=[],
                            ),
                            attr="encode",
                            ctx=ast.Load(),
                        ),
                        args=[ast.Constant("utf-8")],
                        keywords=[],
                    ),
                )
            )
        elif content_type == "application/x-www-form-urlencoded":
            call.keywords.append(
                ast.keyword(
                    "body",
                    ast.Call(
                        func=ast.Name(id="urlencode", ctx=ast.Load()),
                        args=[astify_json_obj(data)],
                        keywords=[],
                    ),
                )
            )
        else:
            call.keywords.append(ast.keyword("body", ast.Constant(data)))

    # Create a PoolManager
    pool_manager = ast.Assign(
        targets=[ast.Name(id="http", ctx=ast.Store())],
        value=ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="urllib3", ctx=ast.Load()),
                attr="PoolManager",
                ctx=ast.Load(),
            ),
            args=[],
            keywords=[],
        ),
    )

    # Response
    response = ast.Assign(targets=[ast.Name(id="r", ctx=ast.Store())], value=call)

    # The whole tree
    tree.body = imports + [pool_manager, response]

    ast.fix_missing_locations(tree)
    return unparse(tree).strip()
