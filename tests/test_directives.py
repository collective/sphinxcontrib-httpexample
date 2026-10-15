from docutils.statemachine import StringList
from sphinx_testing import util
from sphinxcontrib.httpexample import copy_assets
from sphinxcontrib.httpexample.directives import HTTPExample
from unittest.mock import Mock
from unittest.mock import patch
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


def test_copy_assets_skipped_on_non_html():
    app = Mock()
    app.builder.name = "latex"
    with patch("sphinxcontrib.httpexample.shutil.copyfile") as mock_copy:
        copy_assets(app, None)
        mock_copy.assert_not_called()


def test_copy_assets_skipped_on_exception():
    app = Mock()
    app.builder.name = "html"
    with patch("sphinxcontrib.httpexample.shutil.copyfile") as mock_copy:
        copy_assets(app, Exception("build error"))
        mock_copy.assert_not_called()


def test_process_content_empty():
    content = StringList([])
    HTTPExample.process_content(content)
    assert len(content) == 0


def test_directive_response_only():
    with tempdir() as srcdir:
        conf_py = os.path.join(srcdir, "conf.py")
        with open(conf_py, "w", encoding="utf-8") as f:
            f.write(
                "extensions = ['sphinxcontrib.httpdomain', 'sphinxcontrib.httpexample']\n"
                "master_doc = 'index'\n"
                "project = 'test'\n"
            )
        resp_txt = os.path.join(srcdir, "response.txt")
        with open(resp_txt, "w", encoding="utf-8") as f:
            f.write("HTTP/1.1 200 OK\nContent-Type: application/json\n\n{}\n")
        index_rst = os.path.join(srcdir, "index.rst")
        with open(index_rst, "w", encoding="utf-8") as f:
            f.write(
                "Test\n"
                "====\n\n"
                "..  http:example::\n"
                "    :response: response.txt\n"
            )
        with tempdir() as output:
            app = util.TestApp(srcdir=srcdir, outdir=output)
            try:
                app.build()
                with open(
                    os.path.join(app.outdir, "index.html"), encoding="utf-8"
                ) as fp:
                    html = fp.read()
                assert "http-example-response" in html
            finally:
                app.cleanup()
