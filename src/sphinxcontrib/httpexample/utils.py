# -*- coding: utf-8 -*-
from collections import OrderedDict


def ordered(dict_):
    # http://stackoverflow.com/a/22721724
    results = OrderedDict()
    for k, v in sorted(dict_.items()):
        if isinstance(v, dict):
            results[k] = ordered(v)
        else:
            results[k] = v
    return results


def capitalize(s):
    return '-'.join(map(str.capitalize, s.split('-')))


def capitalize_keys(d):
    return dict([(capitalize(k), v) for k, v in d.items()])
