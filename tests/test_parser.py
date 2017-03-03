# -*- coding: utf-8 -*-
import os
import pytest


@pytest.yield_fixture(scope='module')
def fixture(request):
    assert request
    data = {}
    path = os.path.join(os.path.dirname(__file__), 'data')
    for filename in os.listdir(path):
        idx, part = filename.split('.')[:-1]
        data.setdefault(int(idx), {})
        with open(os.path.join(path, filename)) as fp:
            data[int(idx)][part] = fp.read()
    return data


def test_fixture(fixture):
    assert len(fixture)
    for item in fixture.values():
        assert 'request' in item
        assert 'response' in item
