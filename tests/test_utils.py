# -*- coding: utf-8 -*-
import json

from sphinxcontrib.httpexample import utils


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
