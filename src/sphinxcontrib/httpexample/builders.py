# -*- coding: utf-8 -*-
import ast
import astunparse
import json

from sphinxcontrib.httpexample.utils import maybe_str
from sphinxcontrib.httpexample.utils import is_json

try:
    from shlex import quote as shlex_quote
except ImportError:
    from pipes import quote as shlex_quote

EXCLUDE_HEADERS = [
    'Authorization',
    'Host',
]
EXCLUDE_HEADERS_HTTP = EXCLUDE_HEADERS + [
    'Accept',
    'Content-Type'
]
EXCLUDE_HEADERS_REQUESTS = EXCLUDE_HEADERS + [
    'Content-Type'
]


def build_curl_command(request):
    parts = ['curl', '-i']

    # Method
    if request.command != 'GET':
        parts.append('-X {}'.format(request.command))

    # URL
    parts.append(shlex_quote(request.url()))

    # Authorization (prepare)
    method, token = request.auth()

    # Headers
    for header in sorted(request.headers):
        if header in EXCLUDE_HEADERS:
            continue
        header_line = shlex_quote('{}: {}'.format(header, request.headers[header]))
        parts.append('-H {}'.format(header_line))

    if method != 'Basic' and 'Authorization' in request.headers:
        header = 'Authorization'
        header_line = shlex_quote('{}: {}'.format(header, request.headers[header]))
        parts.append('-H {}'.format(header_line))

    # JSON
    data = maybe_str(request.data())
    if data:
        if is_json(request.headers.get('Content-Type', '')):
            data = json.dumps(data)
        parts.append('--data-raw \'{}\''.format(data))

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
        header_line = shlex_quote('{}: {}'.format(header, request.headers[header]))
        parts.append('--header={}'.format(header_line))

    if method != 'Basic' and 'Authorization' in request.headers:
        header = 'Authorization'
        header_line = shlex_quote('{}: {}'.format(header, request.headers[header]))
        parts.append('--header={}'.format(header_line))

    # JSON or raw data
    data = maybe_str(request.data())
    if data:
        if is_json(request.headers.get('Content-Type', '')):
            data = json.dumps(data)
        if request.command == 'POST':
            parts.append('--post-data=\'{}\''.format(data))
        elif request.command != 'POST':
            parts.append('--body-data=\'{}\''.format(data))

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
        parts.append('{}:{}'.format(header, shlex_quote(request.headers[header])))  # noqa

    if method != 'Basic' and 'Authorization' in request.headers:
        header = 'Authorization'
        parts.append('{}:{}'.format(header, shlex_quote(request.headers[header])))  # noqa

    # JSON or raw data
    data = maybe_str(request.data())
    if data:

        if is_json(request.headers.get('Content-Type', '')):
            # We need to explicitly set the separators to get consistent
            # whitespace handling across Python 2 and 3. See
            # https://bugs.python.org/issue16333 for details.
            redir_input = shlex_quote(
                json.dumps(data, indent=2, sort_keys=True, separators=(',', ': ')))
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
    if data:
        if is_json(request.headers.get('Content-Type', '')):
            json_keys = []
            json_values = []
            for k, v in data.items():
                json_keys.append(ast.Str(maybe_str(k)))
                v = maybe_str(v)
                if isinstance(v, str):
                    json_values.append(ast.Str(v))
                else:
                    json_values.append(ast.parse(str(v)).body[0].value)
            if json_keys and json_values:
                call.keywords.append(
                    ast.keyword('json', ast.Dict(json_keys, json_values)))
        else:
            call.keywords.append(ast.keyword('data', ast.Str(data)))

    # Authorization
    if method == 'Basic':
        token = maybe_str(token)
        call.keywords.append(
            ast.keyword('auth', ast.Tuple(
                tuple(map(ast.Str, token.split(':'))), None)))

    return astunparse.unparse(tree).strip()
