# -*- coding: utf-8 -*-
from sphinx_testing import util

import contextlib
import os
import shutil
import tempfile


# http://stackoverflow.com/a/33288373
@contextlib.contextmanager
def cd(newdir, cleanup=lambda: True):
    prev = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prev)
        cleanup()


# http://stackoverflow.com/a/33288373
@contextlib.contextmanager
def tempdir():
    path = tempfile.mkdtemp()

    def cleanup():
        shutil.rmtree(path)

    with cd(path, cleanup):
        yield path


def test_build():
    docs = os.path.join(os.path.dirname(__file__), '..', 'docs')
    with tempdir() as output:
        app = util.TestApp(srcdir=docs, outdir=output)
        try:
            app.build()
            assert 'index.html' in os.listdir(app.outdir)
        finally:
            app.cleanup()


def test_inline_response_parser():
    docs = os.path.join(os.path.dirname(__file__), '..', 'docs')
    with tempdir() as output:
        app = util.TestApp(srcdir=docs, outdir=output)
        try:
            app.build()
            with open(os.path.join(app.outdir, 'usage.html')) as fp:
                assert fp.read().count('http-example-response') == 5
        finally:
            app.cleanup()


def test_loading_request_from_file():
    docs = os.path.join(os.path.dirname(__file__), '..', 'docs')
    with tempdir() as output:
        app = util.TestApp(srcdir=docs, outdir=output)
        try:
            app.build()
            with open(os.path.join(app.outdir, 'usage.html')) as fp:
                result = fp.read()
            result = result.split('Examples with external sources')[-1]
            assert result.count('http-example-http') == 6
            assert result.count('http-example-response') == 3
            assert result.count('http-example-curl') == 3
        finally:
            app.cleanup()
