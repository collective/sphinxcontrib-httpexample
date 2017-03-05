# -*- coding: utf-8 -*-
import os


def read_fixture(filename):
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', filename)) as fp:  # noqa
        return (lambda s: isinstance(s, bytes) and s or s.encode('utf-8'))(fp.read().strip())  # noqa


FIXTURE_001_REQUEST = read_fixture('001.request.txt')
FIXTURE_001_CURL = read_fixture('001.curl.txt')
FIXTURE_001_HTTPIE = read_fixture('001.httpie.txt')
FIXTURE_001_PYTHON_REQUESTS = read_fixture('001.python-requests.txt')
FIXTURE_001_RESPONSE = read_fixture('001.response.txt')

FIXTURE_002_REQUEST = read_fixture('002.request.txt')
FIXTURE_002_CURL = read_fixture('002.curl.txt')
FIXTURE_002_HTTPIE = read_fixture('002.httpie.txt')
FIXTURE_002_PYTHON_REQUESTS = read_fixture('002.python-requests.txt')
FIXTURE_002_RESPONSE = read_fixture('002.response.txt')


def test_fixtures():
    assert isinstance(FIXTURE_001_REQUEST, bytes)
    assert isinstance(FIXTURE_001_CURL, bytes)
    assert isinstance(FIXTURE_001_HTTPIE, bytes)
    assert isinstance(FIXTURE_001_PYTHON_REQUESTS, bytes)
    assert isinstance(FIXTURE_001_RESPONSE, bytes)
