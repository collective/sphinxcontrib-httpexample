# -*- coding: utf-8 -*-
import os


def read_fixture(filename):
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', filename)) as fp:  # noqa
        return (lambda s: isinstance(s, bytes) and s or s.encode('utf-8'))(fp.read())  # noqa


FIXTURE_001_REQUEST = read_fixture('001.request.txt')


def test_fixtures():
    assert isinstance(FIXTURE_001_REQUEST, bytes)
