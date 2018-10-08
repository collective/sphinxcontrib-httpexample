# -*- coding: utf-8 -*-
from io import BytesIO
from sphinxcontrib.httpexample.utils import capitalize_keys
from sphinxcontrib.httpexample.utils import is_json
from sphinxcontrib.httpexample.utils import ordered

import base64
import json
import re

try:
    from urllib import urlencode, unquote
    from urlparse import urlparse, parse_qsl, ParseResult
except: # For Python 3
    from urllib.parse import \
        urlencode, unquote, urlparse, parse_qsl, ParseResult

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
        self.headers = capitalize_keys(dict(self.headers.items()))

    def send_error(self, code, message=None, explain=None):
        self.error_code = code
        self.error_message = message

    def extract_fields(self, field=None):
        if (field is not None) and field not in AVAILABLE_FIELDS:
            msg = "Unexpected field '{}'. Expected one of {}."
            msg = msg.format(field, ', '.join(AVAILABLE_FIELDS))
            raise ValueError(msg)

        if field is None:
            field = '|'.join(AVAILABLE_FIELDS)
        is_field = r':{} (.+): (.+)'.format(field)

        fields = []
        remaining_payload = []
        cursor = self.rfile.tell()
        for i, line in enumerate(self.rfile.readlines()):
            line = line.decode('utf-8')
            try:
                key, val = re.match(is_field, line).groups()
            except AttributeError:
                remaining_payload.append(line)
                continue
            fields.append((key.strip(), val.strip()))

        remaining_payload = BytesIO(
            '\n'.join(remaining_payload).encode('utf-8'))
        self.rfile.seek(cursor)

        return (fields, remaining_payload)

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
        base_url =  '{}://{}{}'.format(
            self.scheme,
            self.headers.get('Host', 'nohost'),
            self.path
        )

        params, _ = self.extract_fields('query')

        if params:
            # https://stackoverflow.com/a/25580545/1262843
            url = unquote(base_url)
            parsed_url = urlparse(url)
            new_params = parse_qsl(parsed_url.query) + params
            new_params_encoded = urlencode(new_params, doseq=True)
            new_url = ParseResult(
                parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                parsed_url.params, new_params_encoded, parsed_url.fragment
            ).geturl()
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
