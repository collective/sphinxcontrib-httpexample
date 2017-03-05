# -*- coding: utf-8 -*-
import ast
import astunparse
import json

from sphinxcontrib.httpexample.utils import maybe_str

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
    parts.append(request.url())

    # Authorization (prepare)
    method, token = request.auth()

    # Headers
    for header in sorted(request.headers):
        if header in EXCLUDE_HEADERS:
            continue
        parts.append('-H "{}: {}"'.format(header, request.headers[header]))
    if method != 'Basic' and 'Authorization' in request.headers:
        header = 'Authorization'
        parts.append('-H "{}: {}"'.format(header, request.headers[header]))

    # JSON
    data = request.data()
    if data:
        parts.append('--data-raw \'{}\''.format(json.dumps(data)))

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
    parts.append(request.url())

    # Authorization (prepare)
    method, token = request.auth()

    # Headers
    for header in sorted(request.headers):
        if header in EXCLUDE_HEADERS:
            continue
        parts.append('--header="{}: {}"'.format(header, request.headers[header]))  # noqa
    if method != 'Basic' and 'Authorization' in request.headers:
        header = 'Authorization'
        parts.append('--header="{}: {}"'.format(header, request.headers[header]))  # noqa

    # JSON
    data = request.data()
    if data and request.command == 'POST':
        parts.append('--post-data=\'{}\''.format(json.dumps(data)))
    elif data and request.command != 'POST':
        parts.append('--body-data=\'{}\''.format(json.dumps(data)))

    # Authorization
    if method == 'Basic':
        user, password = token.split(':')
        parts.append('--auth-no-challenge')
        parts.append('--user={}'.format(user))
        parts.append('--password={}'.format(password))

    return ' '.join(parts)


def build_httpie_command(request):
    parts = ['http', '-j']

    # Method
    if request.command != 'GET':
        parts.append(request.command)

    # URL
    parts.append(request.url())

    # Authorization (prepare)
    method, token = request.auth()

    # Headers
    for header in sorted(request.headers):
        if header in EXCLUDE_HEADERS_HTTP:
            continue
        part = '{}:{}'.format(header, request.headers[header])
        if header == 'Cookie':
            parts.append("'{}'".format(part))
        else:
            parts.append(part)
    if method != 'Basic' and 'Authorization' in request.headers:
        header = 'Authorization'
        parts.append('{}:"{}"'.format(header, request.headers[header]))

    # JSON
    data = request.data() or {}
    for k, v in data.items():
        k = k.replace('@', '\\' * 2 + '@')
        v = maybe_str(v)
        if isinstance(v, str):
            if ' ' in v:
                parts.append('{}="{}"'.format(k, v))
            else:
                parts.append('{}={}'.format(k, v))
        elif any([
            v is None,
            isinstance(v, int),
            isinstance(v, float),
            isinstance(v, bool),
        ]):
            # JSON values
            parts.append('{}:={}'.format(k, json.dumps(v)))
        else:
            # JSON structures
            parts.append("{}:='{}'".format(k, json.dumps(v)))

    # Authorization
    if method == 'Basic':
        parts.append('-a {}'.format(token))

    return ' '.join(parts)


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

    # JSON
    json_keys = []
    json_values = []
    data = request.data() or {}
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

    # Authorization
    if method == 'Basic':
        token = maybe_str(token)
        call.keywords.append(
            ast.keyword('auth', ast.Tuple(
                tuple(map(ast.Str, token.split(':'))), None)))

    return astunparse.unparse(tree).strip()
