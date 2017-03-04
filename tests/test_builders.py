# -*- coding: utf-8 -*-
from sphinxcontrib.httpexample.parsers import parse_request
from sphinxcontrib.httpexample.builders import build_curl_command
from sphinxcontrib.httpexample.builders import build_httpie_command
from sphinxcontrib.httpexample.builders import build_requests_command

from .test_fixtures import FIXTURE_001_REQUEST


def test_curl_fixture_001():
    request = parse_request(FIXTURE_001_REQUEST)
    command = build_curl_command(request)
    assert command == (
        'curl '
        '-i '
        '-X POST http://localhost:8080/Plone/folder '
        '-H "Accept: application/json" '
        '-H "Content-Type: application/json" '
        '--data-raw \'{"@type": "Document", "title": "My Document"}\' '
        '--user admin:admin '
    ).strip()


def test_httpie_fixture_001():
    request = parse_request(FIXTURE_001_REQUEST)
    command = build_httpie_command(request)
    assert command == (
        'http '
        'POST '
        'http://localhost:8080/Plone/folder '
        '\\\\@type=Document title=My Document '
        '-a admin:admin '
    ).strip()


def test_requests_fixture_001():
    request = parse_request(FIXTURE_001_REQUEST)
    command = build_requests_command(request)
    assert command == (
        'requests.post('
        "'http://localhost:8080/Plone/folder', "
        "headers={'Accept': 'application/json'}, "
        "json={'@type': 'Document', 'title': 'My Document'}, "
        "auth=('admin', 'admin')"
        ')'
    ).strip()
