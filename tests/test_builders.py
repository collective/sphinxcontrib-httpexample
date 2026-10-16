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
from sphinxcontrib.httpexample.builders import build_curl_command
from sphinxcontrib.httpexample.builders import build_httpie_command
from sphinxcontrib.httpexample.builders import build_requests_command
from sphinxcontrib.httpexample.builders import build_wget_command
from sphinxcontrib.httpexample.builders import flatten_parsed_qs
from sphinxcontrib.httpexample.builders import shlex_double_quote
from sphinxcontrib.httpexample.builders import shlex_single_quote
from sphinxcontrib.httpexample.parsers import parse_request
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


def test_shlex_double_quote():
    assert shlex_double_quote("") == '""'
    assert shlex_double_quote(None) == '""'


def test_flatten_parsed_qs():
    data = {"a": ["v1", "v2"], "b": ["v3"], "c": "v4"}
    assert flatten_parsed_qs(data) == {"a": ["v1", "v2"], "b": "v3", "c": "v4"}


def test_build_requests_command_no_headers():
    request = parse_request(b"GET /path HTTP/1.1\r\n\r\n")
    cmd = build_requests_command(request)
    assert "headers=" not in cmd


def test_build_requests_command_from_dict_data():
    request = parse_request(
        b"POST /path HTTP/1.1\r\nHost: example.com\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\na=1"
    )
    request.data = lambda: {"a": "1"}
    cmd = build_requests_command(request)
    assert "requests.post" in cmd
    assert "data={'a': '1'}" in cmd


def test_build_requests_command_cannot_astify():
    request = parse_request(
        b"POST /path HTTP/1.1\r\nHost: example.com\r\nContent-Type: application/json\r\n\r\n{}"
    )
    request.data = lambda: object()
    with pytest.raises(Exception, match="Cannot astify"):
        build_requests_command(request)


def test_build_requests_command_json_null_and_primitives():
    request = parse_request(
        b'POST /path HTTP/1.1\r\nHost: example.com\r\nContent-Type: application/json\r\n\r\n{"a": null, "b": true, "c": 42, "d": 3.14}'
    )
    cmd = build_requests_command(request)
    assert "requests.post" in cmd
    assert "'a': None" in cmd
    assert "'b': True" in cmd
    assert "'c': 42" in cmd
    assert "'d': 3.14" in cmd


def test_build_commands_empty_json():
    request = parse_request(
        b"POST /path HTTP/1.1\r\nHost: example.com\r\nContent-Type: application/json\r\n\r\n{}"
    )
    curl_cmd = build_curl_command(request)
    assert "--data-raw '{}'" in curl_cmd
    wget_cmd = build_wget_command(request)
    assert "--post-data='{}'" in wget_cmd
    httpie_cmd = build_httpie_command(request)
    assert "echo '{}' | http" in httpie_cmd
    req_cmd = build_requests_command(request)
    assert "json={}" in req_cmd


def test_shlex_single_quote():
    assert shlex_single_quote("") == "''"
    assert shlex_single_quote('{"a": 1}') == "'{\"a\": 1}'"
    assert shlex_single_quote("it's") == "'it'\"'\"'s'"


@pytest.mark.parametrize(
    "body,httpie_input,requests_json",
    [
        (b"[]", "'[]'", "[]"),
        (b"0", "0", "0"),
        (b"false", "false", "False"),
        (b'""', "'\"\"'", "''"),
    ],
)
def test_build_commands_falsy_json(body, httpie_input, requests_json):
    request = parse_request(
        b"POST /path HTTP/1.1\r\nHost: example.com\r\nContent-Type: application/json\r\n\r\n"
        + body
    )
    literal = body.decode("utf-8")
    assert "--data-raw '{}'".format(literal) in build_curl_command(request)
    assert "--post-data='{}'".format(literal) in build_wget_command(request)
    assert build_httpie_command(request).startswith(
        "echo {} | http POST".format(httpie_input)
    )
    assert "json={})".format(requests_json) in build_requests_command(request)


def test_build_commands_json_null():
    request = parse_request(
        b"POST /path HTTP/1.1\r\nHost: example.com\r\nContent-Type: application/json\r\n\r\nnull"
    )
    assert "--data-raw 'null'" in build_curl_command(request)
    assert "--post-data='null'" in build_wget_command(request)
    assert build_httpie_command(request).startswith("echo null | http POST")
    # json=None would make requests send no body at all
    assert "data='null'" in build_requests_command(request)


def test_build_commands_quote_in_data():
    request = parse_request(
        b"PUT /path HTTP/1.1\r\nHost: example.com\r\nContent-Type: text/plain\r\n\r\nit's"
    )
    assert "--data-raw 'it'\"'\"'s'" in build_curl_command(request)
    assert "--body-data='it'\"'\"'s'" in build_wget_command(request)


def test_build_requests_command_form_without_pairs():
    request = parse_request(
        b"POST /path HTTP/1.1\r\nHost: example.com\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\na"
    )
    assert "data='a'" in build_requests_command(request)
    assert "--data-raw 'a'" in build_curl_command(request)


def test_build_requests_command_form_blank_value_and_charset():
    request = parse_request(
        b"POST /path HTTP/1.1\r\nHost: example.com\r\nContent-Type: application/x-www-form-urlencoded; charset=utf-8\r\n\r\nname=O%27Brien&x=a+b&e="
    )
    assert "data={'name': \"O'Brien\", 'x': 'a b', 'e': ''}" in build_requests_command(
        request
    )


def test_build_commands_basic_auth_password_with_colon():
    request = parse_request(
        b"GET /path HTTP/1.1\r\nHost: example.com\r\nAuthorization: Basic YTpiOmM=\r\n\r\n"
    )
    assert "--user=a --password=b:c" in build_wget_command(request)
    assert "auth=('a', 'b:c')" in build_requests_command(request)


def test_build_requests_command_form_multiple_values():
    request = parse_request(
        b"POST /path HTTP/1.1\r\nHost: example.com\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\na=1&a=2&b=3"
    )
    assert "data={'a': ['1', '2'], 'b': '3'}" in build_requests_command(request)
