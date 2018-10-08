# -*- coding: utf-8 -*-
from io import BytesIO
from sphinxcontrib.httpexample.utils import add_url_params
from sphinxcontrib.httpexample.utils import capitalize_keys
from sphinxcontrib.httpexample.utils import is_json
from sphinxcontrib.httpexample.utils import ordered

import base64
import json
import re


try:
    from http.server import BaseHTTPRequestHandler
except ImportError:
    from BaseHTTPServer import BaseHTTPRequestHandler


AVAILABLE_FIELDS = [
    'query'
]


class HTTPRequest(BaseHTTPRequestHandler):
    # http://stackoverflow.com/a/5955949

    scheme = 'http'

    # noinspection PyMissingConstructor
    def __init__(self, request_bytes, scheme):
        assert isinstance(request_bytes, bytes)

        self.scheme = scheme
        self.rfile = BytesIO(request_bytes)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

        if self.error_message:
            raise Exception(self.error_message)

        # Replace headers with simple dict to coup differences in Py2 and Py3
        self.headers = capitalize_keys(dict(getattr(self, 'headers', {})))

    def send_error(self, code, message=None, explain=None):
        self.error_code = code
        self.error_message = message

    def extract_fields(self, field=None, available_fields=None):
        if available_fields is None:
            available_fields = AVAILABLE_FIELDS

        if (field is not None) and field not in available_fields:
            msg = "Unexpected field '{}'. Expected one of {}."
            msg = msg.format(field, ', '.join(available_fields))
            raise ValueError(msg)

        if field is None:
            field = '|'.join(available_fields)
        is_field = r':({}) (.+): (.+)'.format(field)

        fields = []
        remaining_request = []
        cursor = self.rfile.tell()
        for i, line in enumerate(self.rfile.readlines()):
            line = line.decode('utf-8')
            try:
                field, key, val = re.match(is_field, line).groups()
            except AttributeError:
                remaining_request.append(line)
                continue
            fields.append((field.strip(), key.strip(), val.strip()))

        remaining_request = BytesIO(
            '\n'.join(remaining_request).encode('utf-8').strip())
        remaining_request.seek(0)
        self.rfile.seek(cursor)

        return (fields, remaining_request)

    def auth(self):
        try:
            method, token = self.headers.get('Authorization').split()
        except (AttributeError, KeyError, ValueError):
            return None, None
        if not isinstance(token, bytes):
            token = token.encode('utf-8')
        if method == 'Basic':
            return method, base64.b64decode(token).decode('utf-8')
        else:
            return method, token

    def url(self):
        base_url = '{}://{}{}'.format(
            self.scheme,
            self.headers.get('Host', 'nohost'),
            self.path
        )

        params, _ = self.extract_fields('query')
        params = [(p[1], p[2]) for p in params]

        if params:
            new_url = add_url_params(base_url, params)
        else:
            new_url = base_url

        return new_url

    def data(self):
        _, payload_bytes = self.extract_fields(None)
        payload_bytes = payload_bytes.read()
        if payload_bytes:
            if is_json(self.headers.get('Content-Type', '')):
                assert isinstance(payload_bytes, bytes)
                payload_str = payload_bytes.decode('utf-8')
                return ordered(json.loads(payload_str))
            else:
                return payload_bytes


def parse_request(request_bytes, scheme='http'):
    return HTTPRequest(request_bytes, scheme)
