# -*- coding: utf-8 -*-
from sphinx_testing import util
from sphinxcontrib.httpexample import directives
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
            assert result.count("http-example-http") == 8
            assert result.count("http-example-response") == 3
            assert result.count("http-example-curl") == 4
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


def test_exclude_headers_config(monkeypatch):
    # Keep the builder registered by conf.py from leaking into other tests
    monkeypatch.setattr(
        directives, "AVAILABLE_BUILDERS", dict(directives.AVAILABLE_BUILDERS)
    )
    with tempdir() as srcdir:
        conf_py = os.path.join(srcdir, "conf.py")
        with open(conf_py, "w", encoding="utf-8") as f:
            f.write(
                "extensions = ['sphinxcontrib.httpdomain', 'sphinxcontrib.httpexample']\n"
                "master_doc = 'index'\n"
                "project = 'test'\n"
                "httpexample_exclude_headers = ['x-foo']\n"
                "\n"
                "from sphinxcontrib.httpexample import register_builder\n"
                "\n"
                "def build_echo_command(request):\n"
                "    return 'echo ' + request.headers['X-Foo']\n"
                "\n"
                "register_builder('echo', build_echo_command, 'shell', 'Echo')\n"
            )
        index_rst = os.path.join(srcdir, "index.rst")
        with open(index_rst, "w", encoding="utf-8") as f:
            f.write(
                "Test\n"
                "====\n\n"
                "..  http:example:: curl echo\n\n"
                "    GET /test HTTP/1.1\n"
                "    Host: example.com\n"
                "    Accept: application/json\n"
                "    X-Foo: secretvalue\n"
            )
        with tempdir() as output:
            app = util.TestApp(srcdir=srcdir, outdir=output)
            try:
                app.build()
                with open(
                    os.path.join(app.outdir, "index.html"), encoding="utf-8"
                ) as fp:
                    html = fp.read()

                curl = html.split("http-example-curl")[1].split("http-example-echo")[0]
                assert "Accept" in curl
                assert "secretvalue" not in curl
                echo = html.split("http-example-echo")[1]
                assert "secretvalue" in echo
            finally:
                app.cleanup()
