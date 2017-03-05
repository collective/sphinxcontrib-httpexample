# -*- coding: utf-8 -*-
from sphinxcontrib.httpexample.parsers import parse_request
from sphinxcontrib.httpexample.builders import build_curl_command
from sphinxcontrib.httpexample.builders import build_httpie_command
from sphinxcontrib.httpexample.builders import build_requests_command

from .test_fixtures import FIXTURE_001_REQUEST
from .test_fixtures import FIXTURE_001_CURL
from .test_fixtures import FIXTURE_001_HTTPIE
from .test_fixtures import FIXTURE_001_PYTHON_REQUESTS
from .test_fixtures import FIXTURE_002_REQUEST
from .test_fixtures import FIXTURE_002_CURL
from .test_fixtures import FIXTURE_002_HTTPIE
from .test_fixtures import FIXTURE_002_PYTHON_REQUESTS
from .test_fixtures import FIXTURE_003_REQUEST
from .test_fixtures import FIXTURE_003_CURL
from .test_fixtures import FIXTURE_003_HTTPIE
from .test_fixtures import FIXTURE_003_PYTHON_REQUESTS
from .test_fixtures import FIXTURE_004_REQUEST
from .test_fixtures import FIXTURE_004_CURL
from .test_fixtures import FIXTURE_004_HTTPIE
from .test_fixtures import FIXTURE_004_PYTHON_REQUESTS


def test_curl_fixture_001():
    request = parse_request(FIXTURE_001_REQUEST)
    command = build_curl_command(request)
    assert command == FIXTURE_001_CURL.decode('utf-8')


def test_httpie_fixture_001():
    request = parse_request(FIXTURE_001_REQUEST)
    command = build_httpie_command(request)
    assert command == FIXTURE_001_HTTPIE.decode('utf-8')


def test_requests_fixture_001():
    request = parse_request(FIXTURE_001_REQUEST)
    command = build_requests_command(request)
    assert command == FIXTURE_001_PYTHON_REQUESTS.decode('utf-8')


def test_curl_fixture_002():
    request = parse_request(FIXTURE_002_REQUEST)
    command = build_curl_command(request)
    assert command == FIXTURE_002_CURL.decode('utf-8')


def test_httpie_fixture_002():
    request = parse_request(FIXTURE_002_REQUEST)
    command = build_httpie_command(request)
    assert command == FIXTURE_002_HTTPIE.decode('utf-8')


def test_requests_fixture_002():
    request = parse_request(FIXTURE_002_REQUEST)
    command = build_requests_command(request)
    assert command == FIXTURE_002_PYTHON_REQUESTS.decode('utf-8')


def test_curl_fixture_003():
    request = parse_request(FIXTURE_003_REQUEST)
    command = build_curl_command(request)
    assert command == FIXTURE_003_CURL.decode('utf-8')


def test_httpie_fixture_003():
    request = parse_request(FIXTURE_003_REQUEST)
    command = build_httpie_command(request)
    assert command == FIXTURE_003_HTTPIE.decode('utf-8')


def test_requests_fixture_003():
    request = parse_request(FIXTURE_003_REQUEST)
    command = build_requests_command(request)
    assert command == FIXTURE_003_PYTHON_REQUESTS.decode('utf-8')


def test_curl_fixture_004():
    request = parse_request(FIXTURE_004_REQUEST)
    command = build_curl_command(request)
    assert command == FIXTURE_004_CURL.decode('utf-8')


def test_httpie_fixture_004():
    request = parse_request(FIXTURE_004_REQUEST)
    command = build_httpie_command(request)
    assert command == FIXTURE_004_HTTPIE.decode('utf-8')


def test_requests_fixture_004():
    request = parse_request(FIXTURE_004_REQUEST)
    command = build_requests_command(request)
    assert command == FIXTURE_004_PYTHON_REQUESTS.decode('utf-8')
