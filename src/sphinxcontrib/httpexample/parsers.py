# -*- coding: utf-8 -*-
from io import BytesIO
from sphinxcontrib.httpexample.utils import capitalize_keys
from sphinxcontrib.httpexample.utils import is_json
from sphinxcontrib.httpexample.utils import ordered

import base64
import json


try:
    from http.server import BaseHTTPRequestHandler
except ImportError:
    from BaseHTTPServer import BaseHTTPRequestHandler


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
        self.headers = capitalize_keys(dict(self.headers.items()))

    def send_error(self, code, message=None, explain=None):
        self.error_code = code
        self.error_message = message

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
        return '{}://{}{}'.format(
            self.scheme,
            self.headers.get('Host', 'nohost'),
            self.path
        )

    def data(self):
        payload_bytes = self.rfile.read()
        if payload_bytes:
            if is_json(self.headers.get('Content-Type', '')):
                assert isinstance(payload_bytes, bytes)
                payload_str = payload_bytes.decode('utf-8')
                return ordered(json.loads(payload_str))
            else:
                return payload_bytes


def parse_request(request_bytes, scheme='http'):
    return HTTPRequest(request_bytes, scheme)
