# -*- coding: utf-8 -*-
import base64
import json
import pytest

from sphinxcontrib.httpexample import parsers
from .test_fixtures import FIXTURE_002_REQUEST


def test_parse_request_headers():
    request = parsers.parse_request(FIXTURE_002_REQUEST)
    assert request.command == 'POST'
    assert request.path == '/Plone/folder'
    assert request.request_version == 'HTTP/1.1'

    assert len(request.headers) == 4
    assert request.headers['Host'] == 'localhost:8080'
    assert request.headers['Accept'] == 'application/json'
    assert request.headers['Content-Type'] == 'application/json'
    assert request.headers['Authorization']

    method, token = request.headers['Authorization'].split()
    if not isinstance(token, bytes):
        token = token.encode('utf-8')

    assert method == 'Basic'
    assert token == base64.b64encode(b'admin:admin')


def test_parse_request_url():
    request = parsers.parse_request(FIXTURE_002_REQUEST)
    assert request.url() == 'http://localhost:8080/Plone/folder'


def test_parse_request_auth():
    request = parsers.parse_request(FIXTURE_002_REQUEST)
    assert request.auth() == ('Basic', 'admin:admin')


def test_parse_request_raw():
    request = parsers.parse_request(FIXTURE_002_REQUEST)

    data = request.rfile.read()
    assert isinstance(data, bytes)

    data = json.loads(data.decode('utf-8'))
    assert data == {'@type': 'Document', 'title': 'My Document'}


def test_parse_request_data():
    request = parsers.parse_request(FIXTURE_002_REQUEST)

    data = request.data()
    assert data == {'@type': 'Document', 'title': 'My Document'}


def test_parse_bad_request():
    with pytest.raises(Exception):
        parsers.parse_request(b"""\
POST /Plone/folder
Host: localhost:8080
""")
