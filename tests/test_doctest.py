# -*- coding: utf-8 -*-
import pytest


@pytest.yield_fixture(scope='module')
def rest_mock(request):
    return None


def test_dummy(rest_mock):
    assert True
