# -*- coding: utf-8 -*-
import json

from sphinxcontrib.httpexample import utils


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
