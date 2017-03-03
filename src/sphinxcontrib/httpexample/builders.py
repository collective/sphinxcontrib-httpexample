# -*- coding: utf-8 -*-
import json

from sphinxcontrib.httpexample.utils import capitalize_keys

EXCLUDE_HEADERS = ['Host', 'Authorization']


def build_curl_command(request):
    parts = ['curl', '-i']
    headers = capitalize_keys(dict(request.headers.items()))

    # Method
    if request.command != 'GET':
        parts.append('-X {}'.format(request.command))

    # URL
    parts.append(request.url())

    # Headers
    for header in sorted(headers):
        if header in EXCLUDE_HEADERS:
            continue
        parts.append('-H "{}: {}"'.format(header, headers[header]))

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
    return ''


def build_requests_command(request):
    return ''
