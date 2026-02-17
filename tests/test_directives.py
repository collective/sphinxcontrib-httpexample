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
    docs = os.path.join(os.path.dirname(__file__), "..", "docs")
    with tempdir() as output:
        app = util.TestApp(srcdir=docs, outdir=output)
        try:
            app.build()
            assert "index.html" in os.listdir(app.outdir)
        finally:
            app.cleanup()


def test_inline_response_parser():
    docs = os.path.join(os.path.dirname(__file__), "..", "docs")
    with tempdir() as output:
        app = util.TestApp(srcdir=docs, outdir=output)
        try:
            app.build()
            with open(os.path.join(app.outdir, "usage.html")) as fp:
                assert fp.read().count("http-example-response") == 7
        finally:
            app.cleanup()


def test_loading_request_from_file():
    docs = os.path.join(os.path.dirname(__file__), "..", "docs")
    with tempdir() as output:
        app = util.TestApp(srcdir=docs, outdir=output)
        try:
            app.build()
            with open(os.path.join(app.outdir, "usage.html")) as fp:
                result = fp.read()
            result = result.split("Examples with external sources")[-1]
            assert result.count("http-example-http") == 6
            assert result.count("http-example-response") == 3
            assert result.count("http-example-curl") == 3
        finally:
            app.cleanup()


def test_inline_response_content():
    with tempdir() as srcdir:
        conf_py = os.path.join(srcdir, "conf.py")
        with open(conf_py, "w", encoding="utf-8") as f:
            f.write(
                "extensions = ['sphinxcontrib.httpdomain', 'sphinxcontrib.httpexample']\n"
                "master_doc = 'index'\n"
                "project = 'test'\n"
            )
        index_rst = os.path.join(srcdir, "index.rst")
        with open(index_rst, "w", encoding="utf-8") as f:
            f.write(
                "Test\n"
                "====\n\n"
                "..  http:example-block:: response\n\n"
                "    GET /test HTTP/1.1\n"
                "    Host: example.com\n"
                "    \n"
                "    \n"
                "    HTTP/1.1 200 OK\n"
                "    Content-Type: application/json\n\n"
                "    {}\n"
            )
        with tempdir() as output:
            app = util.TestApp(srcdir=srcdir, outdir=output)
            try:
                app.build()
                with open(
                    os.path.join(app.outdir, "index.html"), encoding="utf-8"
                ) as fp:
                    html = fp.read()

                assert "highlight" in html
            finally:
                app.cleanup()
