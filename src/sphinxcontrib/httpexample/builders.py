# -*- coding: utf-8 -*-
from sphinxcontrib.httpexample.utils import is_json
from sphinxcontrib.httpexample.utils import maybe_str

import ast
import json
import re
import string


try:
    from urllib.parse import parse_qs
except ImportError:
    from urlparse import parse_qs

try:
    from ast import unparse
except ImportError:
    from six.moves import StringIO

    import astunparse

    # Fix: https://github.com/simonpercivall/astunparse/issues/43
    # See: https://github.com/juanlao7/codeclose/commit/0f145f53a3253f9c593c537e1a25c9ef445f30d1  # noqa: E501
    class FixUnparser(astunparse.Unparser):
        def _Constant(self, t):  # noqa:  N802
            if not hasattr(t, 'kind'):
                setattr(t, 'kind', None)
            super()._Constant(t)

    def unparse(tree):
        v = StringIO()
        FixUnparser(tree, file=v)
        return v.getvalue()

try:
    from shlex import quote as shlex_quote
except ImportError:
    from pipes import quote as shlex_quote


_find_unsafe = re.compile(
    r'[^\w@%+=:,./-' + string.ascii_letters + string.digits + ']',
).search


def shlex_double_quote(s):
    """Return a shell-escaped version of the string *s*."""
    if not s:
        return '""'
    if _find_unsafe(s) is None:
        return s

    # use double quotes, and put double quotes into single quotes
    # the string $"b is then quoted as "$"'"'"b"
    return re.sub(r'^""|""$', '', ('"' + s.replace('"', "\"'\"'\"") + '"'))


EXCLUDE_HEADERS = [
    'Authorization',
    'Host',
]
EXCLUDE_HEADERS_HTTP = EXCLUDE_HEADERS + [
]
EXCLUDE_HEADERS_REQUESTS = EXCLUDE_HEADERS + [
]


def build_curl_command(request):
    parts = ['curl', '-i']

    # Method
    parts.append('-X {}'.format(request.command))

    # URL
    parts.append(shlex_quote(request.url()))

    # Authorization (prepare)
    method, token = request.auth()

    # Headers
    for header in sorted(request.headers):
        if header in EXCLUDE_HEADERS:
            continue
        header_line = shlex_double_quote('{}: {}'.format(
            header, request.headers[header]),
        )
        parts.append('-H {}'.format(header_line))

    if method != 'Basic' and 'Authorization' in request.headers:
        header = 'Authorization'
        header_line = shlex_double_quote(
            '{}: {}'.format(header, request.headers[header]),
        )
        parts.append('-H {}'.format(header_line))

    # JSON
    data = maybe_str(request.data())
    if data:
        if is_json(request.headers.get('Content-Type', '')):
            data = json.dumps(data)
        parts.append("--data-raw '{}'".format(data))

    # Authorization
    if method == 'Basic':
        parts.append('--user {}'.format(token))

    return ' '.join(parts)


def build_wget_command(request):
    parts = ['wget', '-S', '-O-']

    # Method
    if request.command not in ['GET', 'POST']:
        parts.append('--method={}'.format(request.command))

    # URL
    parts.append(shlex_quote(request.url()))

    # Authorization (prepare)
    method, token = request.auth()

    # Headers
    for header in sorted(request.headers):
        if header in EXCLUDE_HEADERS:
            continue
        header_line = shlex_double_quote(
            '{}: {}'.format(header, request.headers[header]),
        )
        parts.append('--header={}'.format(header_line))

    if method != 'Basic' and 'Authorization' in request.headers:
        header = 'Authorization'
        header_line = shlex_double_quote(
            '{}: {}'.format(header, request.headers[header])
        )
        parts.append('--header={}'.format(header_line))

    # JSON or raw data
    data = maybe_str(request.data())
    if data:
        if is_json(request.headers.get('Content-Type', '')):
            data = json.dumps(data)
        if request.command == 'POST':
            parts.append("--post-data='{}'".format(data))
        elif request.command != 'POST':
            parts.append("--body-data='{}'".format(data))

    # Authorization
    if method == 'Basic':
        user, password = token.split(':')
        parts.append('--auth-no-challenge')
        parts.append('--user={}'.format(user))
        parts.append('--password={}'.format(password))

    return ' '.join(parts)


def build_httpie_command(request):
    parts = ['http']
    redir_input = ''

    # Method
    if request.command != 'GET':
        parts.append(request.command)

    # URL
    parts.append(shlex_quote(request.url()))

    # Authorization (prepare)
    method, token = request.auth()

    # Headers
    for header in sorted(request.headers):
        if header in EXCLUDE_HEADERS_HTTP:
            continue
        parts.append('{}:{}'.format(
            header, shlex_double_quote(request.headers[header]),
        ))

    if method != 'Basic' and 'Authorization' in request.headers:
        header = 'Authorization'
        parts.append('{}:{}'.format(
            header, shlex_double_quote(request.headers[header]),
        ))

    # JSON or raw data
    data = maybe_str(request.data())
    if data:

        if is_json(request.headers.get('Content-Type', '')):
            # We need to explicitly set the separators to get consistent
            # whitespace handling across Python 2 and 3. See
            # https://bugs.python.org/issue16333 for details.
            redir_input = shlex_quote(
                json.dumps(data, indent=2, sort_keys=True,
                           separators=(',', ': ')))
        else:
            redir_input = shlex_quote(data)

    # Authorization
    if method == 'Basic':
        parts.append('-a {}'.format(token))

    cmd = ' '.join(parts)

    if not redir_input:
        return cmd

    else:
        return 'echo {} | {}'.format(redir_input, cmd)


def build_plone_javascript_command(request):
    javascript_code = 'createAliasesMutation'
    redir_input2 = ''

    # Request body
    data = maybe_str(request.data())
    if data:
        if is_json(request.headers.get('Content-Type', '')):
            redir_input2 = json.dumps(
                data, indent=2, sort_keys=True,
                separators=(',', ': '),
            ).encode('utf-8')
        else:
            redir_input2 = data

    # Output string
    output_string =\
        "{}\n|\nconst aliasesData = '{}';".format(
            maybe_str(javascript_code),
            maybe_str(redir_input2),
        )

    return output_string


def flatten_parsed_qs(data):
    """Flatten single value lists in parse_qs results."""
    for key, value in data.items():
        if isinstance(value, list) and len(value) == 1:
            data[key] = value[0]
    return data


def build_requests_command(request):
    # Method
    tree = ast.parse('requests.{}()'.format(request.command.lower()))
    call = tree.body[0].value
    call.keywords = []

    # URL
    call.args.append(ast.Str(request.url()))

    # Authorization (prepare)
    method, token = request.auth()

    # Headers
    header_keys = []
    header_values = []
    for header in sorted(request.headers):
        if header in EXCLUDE_HEADERS_REQUESTS:
            continue
        header_keys.append(ast.Str(header))
        header_values.append(ast.Str(request.headers[header]))
    if method != 'Basic' and 'Authorization' in request.headers:
        header_keys.append(ast.Str('Authorization'))
        header_values.append(ast.Str(request.headers['Authorization']))
    if header_keys and header_values:
        call.keywords.append(
            ast.keyword('headers', ast.Dict(header_keys, header_values)))

    # JSON or raw data
    data = maybe_str(request.data())

    # Form data
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/x-www-form-urlencoded':
        if not isinstance(data, dict):
            data = flatten_parsed_qs(parse_qs(data))

    def astify_json_obj(obj):
        obj = maybe_str(obj)
        if isinstance(obj, str):
            return ast.Str(obj)
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
                json_keys.append(ast.Str(maybe_str(k)))
                json_values.append(astify_json_obj(v))
            return ast.Dict(json_keys, json_values)
        else:
            raise Exception('Cannot astify {0:s}'.format(str(obj)))

    if data:
        if is_json(request.headers.get('Content-Type', '')):
            call.keywords.append(ast.keyword('json', astify_json_obj(data)))
        else:
            call.keywords.append(ast.keyword('data', ast.Str(data)))

    # Authorization
    if method == 'Basic':
        token = maybe_str(token)
        call.keywords.append(
            ast.keyword('auth', ast.Tuple(
                tuple(map(ast.Str, token.split(':'))), None)))

    return unparse(tree).strip()
