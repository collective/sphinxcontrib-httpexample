# -*- coding: utf-8 -*-
import json

from sphinxcontrib.httpexample import utils


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
    assert json.dumps(utils.ordered(data), indent=4) == """\
{
    "a": {
        "b": {},
        "c": {}
    },
    "d": {
        "e": {},
        "f": {}
    }
}"""
