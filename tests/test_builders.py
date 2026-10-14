# -*- coding: utf-8 -*-
from .test_fixtures import FIXTURE_001_REQUEST
from .test_fixtures import FIXTURE_002_REQUEST
from .test_fixtures import FIXTURE_003_REQUEST
from .test_fixtures import FIXTURE_004_REQUEST
from .test_fixtures import FIXTURE_005_REQUEST
from .test_fixtures import FIXTURE_006_REQUEST
from .test_fixtures import FIXTURE_007_REQUEST
from .test_fixtures import FIXTURE_008_REQUEST
from .test_fixtures import FIXTURE_009_REQUEST
from .test_fixtures import FIXTURE_011_REQUEST
from .test_fixtures import FIXTURE_012_REQUEST
from .test_fixtures import FIXTURE_013_REQUEST
from .test_fixtures import FIXTURE_014_REQUEST
from sphinxcontrib.httpexample import builders
from sphinxcontrib.httpexample.builders import build_curl_command
from sphinxcontrib.httpexample.builders import build_httpie_command
from sphinxcontrib.httpexample.builders import build_requests_command
from sphinxcontrib.httpexample.builders import build_wget_command
from sphinxcontrib.httpexample.parsers import parse_request
import importlib
import pytest


request_fixtures = (
    {"name": "fixture_001", "data": FIXTURE_001_REQUEST},
    {"name": "fixture_002", "data": FIXTURE_002_REQUEST},
    {"name": "fixture_003", "data": FIXTURE_003_REQUEST},
    {"name": "fixture_004", "data": FIXTURE_004_REQUEST},
    {"name": "fixture_005", "data": FIXTURE_005_REQUEST},
    {"name": "fixture_006", "data": FIXTURE_006_REQUEST},
    {"name": "fixture_007", "data": FIXTURE_007_REQUEST},
    {"name": "fixture_008", "data": FIXTURE_008_REQUEST},
    {"name": "fixture_009", "data": FIXTURE_009_REQUEST},
    {"name": "fixture_011", "data": FIXTURE_011_REQUEST},
    {"name": "fixture_012", "data": FIXTURE_012_REQUEST},
    {"name": "fixture_013", "data": FIXTURE_013_REQUEST},
    {"name": "fixture_014", "data": FIXTURE_014_REQUEST},
)


@pytest.mark.parametrize(
    "request_fixture",
    request_fixtures,
    ids=[fixture["name"] for fixture in request_fixtures],
)
@pytest.mark.parametrize(
    "builder",
    (
        build_httpie_command,
        build_curl_command,
        build_wget_command,
        build_requests_command,
    ),
    ids=lambda fn: fn.__name__,
)
def test_fixture(request_fixture, builder, snapshot):
    command = builder(parse_request(request_fixture["data"]))
    snapshot.assert_match(command)


@pytest.mark.parametrize(
    "environ,expected",
    (
        ({}, []),
        ({"HTTP_EXAMPLE_EXCLUDE_HEADERS": ""}, []),
        ({"HTTP_EXAMPLE_EXCLUDE_HEADERS": " , "}, []),
        ({"HTTP_EXAMPLE_EXCLUDE_HEADERS": "x-foo"}, ["X-Foo"]),
        ({"HTTP_EXAMPLE_EXCLUDE_HEADERS": "x-foo, X-BAR"}, ["X-Foo", "X-Bar"]),
    ),
)
def test_get_env_exclude_headers(environ, expected):
    assert builders.get_env_exclude_headers(environ) == expected


@pytest.fixture
def exclude_headers_env(monkeypatch):
    monkeypatch.setenv("HTTP_EXAMPLE_EXCLUDE_HEADERS", "x-foo")
    importlib.reload(builders)
    yield
    monkeypatch.delenv("HTTP_EXAMPLE_EXCLUDE_HEADERS")
    importlib.reload(builders)


def test_exclude_headers_from_env(exclude_headers_env):
    assert "X-Foo" in builders.EXCLUDE_HEADERS
    assert "X-Foo" in builders.EXCLUDE_HEADERS_HTTP
    assert "X-Foo" in builders.EXCLUDE_HEADERS_REQUESTS


@pytest.mark.parametrize(
    "builder",
    (
        build_httpie_command,
        build_curl_command,
        build_wget_command,
        build_requests_command,
    ),
    ids=lambda fn: fn.__name__,
)
def test_exclude_headers(builder, exclude_headers_env):
    request = parse_request(
        b"GET /Plone HTTP/1.1\r\n"
        b"Host: localhost:8080\r\n"
        b"Accept: application/json\r\n"
        b"x-foo: secretvalue\r\n"
        b"\r\n"
    )
    # Custom builders still see the excluded header
    assert request.headers["X-Foo"] == "secretvalue"
    command = builder(request)
    assert "Accept" in command
    assert "X-Foo" not in command
    assert "secretvalue" not in command
