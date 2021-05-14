# -*- coding: utf-8 -*-
from sphinxcontrib.httpexample import utils

import json
import os
import pytest


def test_merge_dicts():
    assert utils.merge_dicts({'a': 'b'}, {'c': 'd'}) == {'a': 'b', 'c': 'd'}
    assert utils.merge_dicts({'a': 'b'}, {'a': 'c'}) == {'a': 'c'}


def test_resolve_path():
    cwd = os.path.dirname(__file__)
    base = os.path.basename(__file__)
    assert utils.resolve_path(base, cwd) == __file__
    assert utils.resolve_path('sphinxcontrib.httpexample:utils.py') == utils.__file__  # noqa
    assert utils.resolve_path('bar', 'non-existing') == 'bar'


def test_maybe_str():
    assert isinstance(utils.maybe_str(b''), str)
    assert isinstance(utils.maybe_str(b''.decode('utf-8')), str)
    assert isinstance(utils.maybe_str(''), str)
    assert not isinstance(utils.maybe_str(1), str)


def test_capitalize():
    assert utils.capitalize('authorization') == 'Authorization'
    assert utils.capitalize('content-type') == 'Content-Type'


def test_capitalize_dict():
    d = {'content-type': 'application/json'}
    assert utils.capitalize_keys(d) == {
        'Content-Type': 'application/json'
    }


def test_ordered():
    data = {
        'd': {
            'f': {},
            'e': {}
        },
        'a': {
            'c': {},
            'b': {}
        }
    }
    assert json.dumps(utils.ordered(data)) == \
        '{"a": {"b": {}, "c": {}}, "d": {"e": {}, "f": {}}}'


def test_add_url_params():
    url = 'www.api.com/items'
    params = [('from', '20180101'), ('to', '20180131')]

    expected = 'www.api.com/items?from=20180101&to=20180131'
    actual = utils.add_url_params(url, params)
    assert expected == actual

    url = url + '?user_id=2'
    params += [('user_id', 3)]
    expected = ('www.api.com/items?user_id=2&from=20180101'
                '&to=20180131&user_id=3')
    actual = utils.add_url_params(url, params)
    assert expected == actual

    params += [('user_id', 4)]
    expected = expected + '&user_id=4'
    actual = utils.add_url_params(url, params)
    assert expected == actual


@pytest.mark.parametrize('ctype,expected', (
 ('application/json', True),
 ('application/json; charset=utf-8', True),
 ('application/vnd.acme+json', True),
 ('application/vnd.acme+json; charset=utf-8; profile="/foo.schema"', True),
 ('application/octet-stream', False),
 ('', False),
))
def test_is_json(ctype, expected):
    assert utils.is_json(ctype) is expected
