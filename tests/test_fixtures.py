# -*- coding: utf-8 -*-
import os


def read_fixture(filename):
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', filename)) as fp:  # noqa
        return (lambda s: isinstance(s, bytes) and s or s.encode('utf-8'))(fp.read().strip())  # noqa


FIXTURE_001_REQUEST = read_fixture('001.request.txt')
FIXTURE_001_CURL = read_fixture('001.curl.txt')
FIXTURE_001_WGET = read_fixture('001.wget.txt')
FIXTURE_001_HTTPIE = read_fixture('001.httpie.txt')
FIXTURE_001_PYTHON_REQUESTS = read_fixture('001.python-requests.txt')
FIXTURE_001_RESPONSE = read_fixture('001.response.txt')

FIXTURE_002_REQUEST = read_fixture('002.request.txt')
FIXTURE_002_CURL = read_fixture('002.curl.txt')
FIXTURE_002_WGET = read_fixture('002.wget.txt')
FIXTURE_002_HTTPIE = read_fixture('002.httpie.txt')
FIXTURE_002_PYTHON_REQUESTS = read_fixture('002.python-requests.txt')
FIXTURE_002_RESPONSE = read_fixture('002.response.txt')

FIXTURE_003_REQUEST = read_fixture('003.request.txt')
FIXTURE_003_CURL = read_fixture('003.curl.txt')
FIXTURE_003_WGET = read_fixture('003.wget.txt')
FIXTURE_003_HTTPIE = read_fixture('003.httpie.txt')
FIXTURE_003_PYTHON_REQUESTS = read_fixture('003.python-requests.txt')
FIXTURE_003_RESPONSE = read_fixture('003.response.txt')

FIXTURE_004_REQUEST = read_fixture('004.request.txt')
FIXTURE_004_CURL = read_fixture('004.curl.txt')
FIXTURE_004_WGET = read_fixture('004.wget.txt')
FIXTURE_004_HTTPIE = read_fixture('004.httpie.txt')
FIXTURE_004_PYTHON_REQUESTS = read_fixture('004.python-requests.txt')
FIXTURE_004_RESPONSE = read_fixture('004.response.txt')

FIXTURE_005_REQUEST = read_fixture('005.request.txt')
FIXTURE_005_CURL = read_fixture('005.curl.txt')
FIXTURE_005_WGET = read_fixture('005.wget.txt')
FIXTURE_005_HTTPIE = read_fixture('005.httpie.txt')
FIXTURE_005_PYTHON_REQUESTS = read_fixture('005.python-requests.txt')
FIXTURE_005_RESPONSE = read_fixture('005.response.txt')


def test_fixtures():
    assert isinstance(FIXTURE_001_REQUEST, bytes)
    assert isinstance(FIXTURE_001_CURL, bytes)
    assert isinstance(FIXTURE_001_HTTPIE, bytes)
    assert isinstance(FIXTURE_001_PYTHON_REQUESTS, bytes)
    assert isinstance(FIXTURE_001_RESPONSE, bytes)
