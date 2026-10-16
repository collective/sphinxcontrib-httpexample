# -*- coding: utf-8 -*-
from .test_fixtures import FIXTURE_002_REQUEST
from .test_fixtures import FIXTURE_010_REQUEST
from .test_fixtures import FIXTURE_011_REQUEST
from sphinxcontrib.httpexample import parsers
import base64
import json
import pytest


def test_parse_request_headers():
    request = parsers.parse_request(FIXTURE_002_REQUEST)
    assert request.command == "POST"
    assert request.path == "/Plone/folder"
    assert request.request_version == "HTTP/1.1"

    assert len(request.headers) == 4
    assert request.headers["Host"] == "localhost:8080"
    assert request.headers["Accept"] == "application/json"
    assert request.headers["Content-Type"] == "application/json"
    assert request.headers["Authorization"]

    method, token = request.headers["Authorization"].split()
    if not isinstance(token, bytes):
        token = token.encode("utf-8")

    assert method == "Basic"
    assert token == base64.b64encode(b"admin:admin")


def test_parse_request_url():
    request = parsers.parse_request(FIXTURE_002_REQUEST)
    assert request.url() == "http://localhost:8080/Plone/folder"


def test_parse_request_url_https():
    request = parsers.parse_request(FIXTURE_002_REQUEST, "https")
    assert request.url() == "https://localhost:8080/Plone/folder"


def test_parse_request_auth():
    request = parsers.parse_request(FIXTURE_002_REQUEST)
    assert request.auth() == ("Basic", "admin:admin")


def test_parse_request_auth_bearer():
    request = parsers.parse_request(
        b"GET / HTTP/1.1\r\nHost: example.com\r\nAuthorization: Bearer mytoken\r\n\r\n"
    )
    assert request.auth() == ("Bearer", "mytoken")


def test_parse_request_auth_none():
    request = parsers.parse_request(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
    assert request.auth() == (None, None)


def test_parse_request_auth_invalid_basic():
    request = parsers.parse_request(
        b"GET / HTTP/1.1\r\nHost: example.com\r\nAuthorization: Basic not_base64!\r\n\r\n"
    )
    assert request.auth() == (None, None)


def test_parse_request_auth_malformed():
    request = parsers.parse_request(
        b"GET / HTTP/1.1\r\nHost: example.com\r\nAuthorization: Bearer\r\n\r\n"
    )
    assert request.auth() == (None, None)


def test_parse_request_raw():
    request = parsers.parse_request(FIXTURE_002_REQUEST)

    data = request.rfile.read()
    assert isinstance(data, bytes)

    data = json.loads(data.decode("utf-8"))
    assert data == {"@type": "Document", "title": "My Document"}


def test_parse_request_data():
    request = parsers.parse_request(FIXTURE_002_REQUEST)

    data = request.data()
    assert data == {"@type": "Document", "title": "My Document"}


def test_parse_request_data_text_plain():
    request = parsers.parse_request(
        b"POST /path HTTP/1.1\r\nHost: example.com\r\nContent-Type: text/plain\r\n\r\nHello World"
    )
    assert request.data() == "Hello World"
    assert isinstance(request.data(), str)


def test_parse_request_data_empty():
    request = parsers.parse_request(b"GET /path HTTP/1.1\r\nHost: example.com\r\n\r\n")
    assert request.data() is None
    assert request.has_data() is False


def test_parse_request_data_json_null():
    request = parsers.parse_request(
        b"POST /path HTTP/1.1\r\nHost: example.com\r\nContent-Type: application/json\r\n\r\nnull"
    )
    assert request.data() is None
    assert request.has_data() is True


@pytest.mark.parametrize("method", ["extract_fields", "has_data", "data"])
def test_parse_request_data_invalid_utf8(method):
    request = parsers.parse_request(
        b"POST /path HTTP/1.1\r\nHost: example.com\r\nContent-Type: text/plain\r\n\r\n\xff"
    )
    # body lines are decoded strictly in extract_fields
    with pytest.raises(UnicodeDecodeError):
        getattr(request, method)()


@pytest.mark.parametrize("eol", [b"\n", b"\r\n"])
def test_parse_request_data_multiline(eol):
    request = parsers.parse_request(
        b"POST /path HTTP/1.1\r\nHost: example.com\r\nContent-Type: text/plain\r\n\r\n"
        + b"line1"
        + eol
        + b"line2"
    )
    assert request.data() == (b"line1" + eol + b"line2").decode("utf-8")


def test_parse_bad_request():
    with pytest.raises(Exception):
        parsers.parse_request(b"""\
POST /Plone/folder
Host: localhost:8080
""")


def test_parse_json_list():
    request = parsers.parse_request(FIXTURE_010_REQUEST)

    data = request.data()
    assert data == [{"@type": "Document", "title": "My Document"}]


def test_parse_extract_fields():
    # known valid request
    request = parsers.parse_request(FIXTURE_011_REQUEST)
    fields, remainder = request.extract_fields("query")

    expected = [
        ("query", "from", "20170101"),
        ("query", "to", "20171231"),
        ("query", "user_id", "15"),
        ("query", "limit", "20"),
        ("query", "sort", "date-asc"),
    ]
    actual = fields
    assert expected == actual

    expected = b""
    actual = remainder.read()
    assert expected == actual

    # potential future request
    add = b"\n:some-future-field foo: bar\n\nfoo-bar"
    request_future_proof = FIXTURE_011_REQUEST + add
    request = parsers.parse_request(request_future_proof)
    fields, remainder = request.extract_fields(
        field=None, available_fields=["query", "some-future-field"]
    )

    expected = [
        ("query", "from", "20170101"),
        ("query", "to", "20171231"),
        ("query", "user_id", "15"),
        ("query", "limit", "20"),
        ("query", "sort", "date-asc"),
        ("some-future-field", "foo", "bar"),
    ]
    actual = fields
    assert expected == actual

    expected = b"foo-bar"
    actual = remainder.read()
    assert expected == actual

    # invalid request
    add = b"\n:invalid-field foo: bar\n\nfoo-bar"
    request_invalid_field = FIXTURE_011_REQUEST + add
    request = parsers.parse_request(request_invalid_field)

    with pytest.raises(ValueError):
        fields, remainder = request.extract_fields(
            field="invalid-field", available_fields=["query", "some-future-field"]
        )
