# -*- coding: utf-8 -*-
import json

EXCLUDE_HEADERS = [
    'Authorization',
    'Host',
]
EXCLUDE_HEADERS_HTTP = EXCLUDE_HEADERS + [
    'Accept',
    'Content-Type'
]


def build_curl_command(request):
    parts = ['curl', '-i']

    # Method
    if request.command != 'GET':
        parts.append('-X {}'.format(request.command))

    # URL
    parts.append(request.url())

    # Headers
    for header in sorted(request.headers):
        if header in EXCLUDE_HEADERS:
            continue
        parts.append('-H "{}: {}"'.format(header, request.headers[header]))

    # JSON
    data = request.data()
    if data:
        parts.append('--data-raw \'{}\''.format(json.dumps(data)))

    # Authorization
    method, token = request.auth()
    if method == 'Basic':
        parts.append('--user {}'.format(token))

    return ' '.join(parts)


def build_httpie_command(request):
    parts = ['http']

    # Method
    if request.command != 'GET':
        parts.append(request.command)

    # URL
    parts.append(request.url())

    # Headers
    for header in sorted(request.headers):
        if header in EXCLUDE_HEADERS_HTTP:
            continue
        part = '{}:{}'.format(header, request.headers[header])
        if header == 'Cookie':
            parts.append("'{}'".format(part))
        else:
            parts.append(part)

    # JSON
    data = request.data() or {}
    for k, v in data.items():
        k = k.replace('@', '\\' * 2 + '@')
        if isinstance(v, str):
            # String values
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
    method, token = request.auth()
    if method == 'Basic':
        parts.append('-a {}'.format(token))

    return ' '.join(parts)

def build_requests_command(request):
    return ''
