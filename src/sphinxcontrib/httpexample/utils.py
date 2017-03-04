# -*- coding: utf-8 -*-
from collections import OrderedDict

import pkg_resources
import os


def merge_dicts(a, b):
    c = a.copy()
    c.update(b)
    return c


def resolve_path(spec, cwd=''):
    if os.path.isfile(os.path.normpath(os.path.join(cwd, spec))):
        return os.path.normpath(os.path.join(cwd, spec))
    elif (spec.count(':') and
          pkg_resources.resource_exists(*spec.split(':', 1))):
        return pkg_resources.resource_filename(*spec.split(':', 1))
    else:
        return spec


def maybe_str(v):
    """Convert any strings to local 'str' instances"""
    if isinstance(v, str) and isinstance(v, bytes):
        return v                  # Python 2 encoded
    elif str(type(v)) == "<type 'unicode'>":
        return v.encode('utf-8')  # Python 2 unicode
    elif isinstance(v, bytes):
        return v.decode('utf-8')  # Python 3 encoded
    elif isinstance(v, str):
        return v                  # Python 3 unicode
    else:
        return v                  # not a string


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
