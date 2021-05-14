# -*- coding: utf-8 -*-
from collections import OrderedDict

import os
import pkg_resources


try:
    from urllib import unquote
    from urllib import urlencode
    from urlparse import parse_qsl
    from urlparse import ParseResult
    from urlparse import urlparse
except ImportError:
    from urllib.parse import parse_qsl
    from urllib.parse import ParseResult
    from urllib.parse import unquote
    from urllib.parse import urlencode
    from urllib.parse import urlparse


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
    if isinstance(dict_, dict):
        # http://stackoverflow.com/a/22721724
        results = OrderedDict()
        for k, v in sorted(dict_.items()):
            results[k] = ordered(v)
    else:
        results = dict_
    return results


def capitalize(s):
    return '-'.join(map(str.capitalize, s.split('-')))


def capitalize_keys(d):
    return dict([(capitalize(k), v) for k, v in d.items()])


def is_json(content_type):
    """Checks if the given content type should be treated as JSON.

    The primary use cases to be recognized as JSON are

    - `application/json` mimetype
    - `+json` structured syntax suffix
    """
    parts = {part.strip() for part in content_type.lower().strip().split(';')}
    if 'application/json' in parts:
        return True

    for p in parts:
        if p.endswith('+json'):
            return True

    return False


def add_url_params(url, params):
    """Add GET query parameters to provided URL.

    https://stackoverflow.com/a/25580545/1262843

    Args:
        url (str): target URL
        params (list of tuples): query parameters to be added

    Returns:
        new_url (str): updated URL
    """
    url = unquote(url)
    parsed_url = urlparse(url)
    new_params = parse_qsl(parsed_url.query) + params
    new_params_encoded = urlencode(new_params, doseq=True)
    new_url = ParseResult(
        parsed_url.scheme, parsed_url.netloc, parsed_url.path,
        parsed_url.params, new_params_encoded, parsed_url.fragment
    ).geturl()

    return new_url
