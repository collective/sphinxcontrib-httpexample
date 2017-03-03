# -*- coding: utf-8 -*-
import pkg_resources


def setup(app):
    dist = pkg_resources.get_distribution('sphinxcontrib_httpexample')
    return {'version': dist.version}
