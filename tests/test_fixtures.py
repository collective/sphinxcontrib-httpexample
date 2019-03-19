# -*- coding: utf-8 -*-
import os


def read_fixture(filename):
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', filename)) as fp:  # noqa
        return (lambda s: isinstance(s, bytes) and s or s.encode('utf-8'))(fp.read().strip())  # noqa


FIXTURE_001_REQUEST = read_fixture('001.request.txt')
FIXTURE_001_RESPONSE = read_fixture('001.response.txt')

FIXTURE_002_REQUEST = read_fixture('002.request.txt')
FIXTURE_002_RESPONSE = read_fixture('002.response.txt')

FIXTURE_003_REQUEST = read_fixture('003.request.txt')
FIXTURE_003_RESPONSE = read_fixture('003.response.txt')

FIXTURE_004_REQUEST = read_fixture('004.request.txt')
FIXTURE_004_RESPONSE = read_fixture('004.response.txt')

FIXTURE_005_REQUEST = read_fixture('005.request.txt')
FIXTURE_005_RESPONSE = read_fixture('005.response.txt')

FIXTURE_006_REQUEST = read_fixture('006.request.txt')
FIXTURE_006_RESPONSE = read_fixture('006.response.txt')

FIXTURE_007_REQUEST = read_fixture('007.request.txt')
FIXTURE_007_RESPONSE = read_fixture('007.response.txt')

FIXTURE_008_REQUEST = read_fixture('008.request.txt')
FIXTURE_009_REQUEST = read_fixture('009.request.txt')
FIXTURE_010_REQUEST = read_fixture('010.request.txt')
FIXTURE_011_REQUEST = read_fixture('011.request.txt')
FIXTURE_012_REQUEST = read_fixture('012.request.txt')


def test_fixtures():
    assert isinstance(FIXTURE_001_REQUEST, bytes)
    assert isinstance(FIXTURE_001_RESPONSE, bytes)
