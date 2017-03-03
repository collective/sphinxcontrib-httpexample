# -*- coding: utf-8 -*-
import base64
import json
import os
import pytest

from sphinxcontrib.httpexample import parsers


@pytest.yield_fixture(scope='module')
def fixture(request):
    assert request
    data = {}
    path = os.path.join(os.path.dirname(__file__), 'data')
    for filename in os.listdir(path):
        idx, part = filename.split('.')[:-1]
        data.setdefault(idx, {})
        with open(os.path.join(path, filename)) as fp:
            data[idx][part] = fp.read()
            if not isinstance(data[idx][part], bytes):
                data[idx][part] = data[idx][part].encode('utf-8')
    return data


# noinspection PyShadowingNames
def test_fixture(fixture):
    assert len(fixture)
    for item in fixture.values():
        assert 'request' in item
        assert 'response' in item
        for value in item.values():
            assert isinstance(value, bytes)


# noinspection PyShadowingNames
def test_parse_request_headers(fixture):
    request = parsers.parse_request(fixture['001']['request'])
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


# noinspection PyShadowingNames
def test_parse_request_url(fixture):
    request = parsers.parse_request(fixture['001']['request'])
    assert request.url() == 'http://localhost:8080/Plone/folder'


# noinspection PyShadowingNames
def test_parse_request_auth(fixture):
    request = parsers.parse_request(fixture['001']['request'])
    assert request.auth() == ('Basic', 'admin:admin')


# noinspection PyShadowingNames
def test_parse_request_payload(fixture):
    request = parsers.parse_request(fixture['001']['request'])

    data = request.rfile.read()
    assert isinstance(data, bytes)

    data = json.loads(data.decode('utf-8'))
    assert data == {'@type': 'Document', 'title': 'My Document'}


# noinspection PyShadowingNames
def test_parse_request_json(fixture):
    request = parsers.parse_request(fixture['001']['request'])

    data = request.data()
    assert data == {'@type': 'Document', 'title': 'My Document'}
