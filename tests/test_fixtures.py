# -*- coding: utf-8 -*-

FIXTURE_001_REQUEST = b"""\
POST /Plone/folder HTTP/1.1
Host: localhost:8080
Accept: application/json
Content-Type: application/json
Authorization: Basic YWRtaW46YWRtaW4=

{
    "@type": "Document",
    "title": "My Document"
}
"""


def test_fixtures():
    assert isinstance(FIXTURE_001_REQUEST, bytes)
