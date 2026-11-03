from docutils.statemachine import StringList
from io import StringIO
from sphinx_testing import util
from sphinxcontrib.httpexample import copy_assets
from sphinxcontrib.httpexample import directives
from sphinxcontrib.httpexample.directives import HTTPExample
from unittest.mock import Mock
from unittest.mock import patch
import contextlib
import os
import pytest
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


BUILDER_ARGS_CONF_PY = """\
extensions = [
    'myst_parser',
    'sphinxcontrib.httpdomain',
    'sphinxcontrib.httpexample',
]
master_doc = 'index'
project = 'test'

from sphinxcontrib.httpexample import register_builder

def build_echo_command(request, method=None, timeout=None, retry=None):
    return 'echo method={} attempts={}'.format(
        method, (retry or {}).get('attempts')
    )

register_builder('echo', build_echo_command, 'text', 'Echo')

def build_kwargs_command(request, **kwargs):
    return 'kwargs {}'.format(','.join(sorted(kwargs)))

register_builder('kwargs', build_kwargs_command, 'text', 'Kwargs')
"""


def build_builder_args(monkeypatch, directive, filename="index.rst", files=None):
    # Keep the builder registered by conf.py from leaking into other tests
    monkeypatch.setattr(
        directives, "AVAILABLE_BUILDERS", dict(directives.AVAILABLE_BUILDERS)
    )
    with tempdir() as srcdir:
        with open(os.path.join(srcdir, "conf.py"), "w", encoding="utf-8") as f:
            f.write(BUILDER_ARGS_CONF_PY)
        with open(os.path.join(srcdir, filename), "w", encoding="utf-8") as f:
            f.write("Test\n====\n\n" + directive)
        for name, content in (files or {}).items():
            with open(os.path.join(srcdir, name), "w", encoding="utf-8") as f:
                f.write(content)
        with tempdir() as output:
            warning = StringIO()
            app = util.TestApp(srcdir=srcdir, outdir=output, warning=warning)
            try:
                app.build()
                with open(
                    os.path.join(app.outdir, "index.html"), encoding="utf-8"
                ) as fp:
                    return fp.read(), warning.getvalue()
            finally:
                app.cleanup()


REQUEST = (
    "\n"
    "    POST /Plone/folder HTTP/1.1\n"
    "    Host: localhost:8080\n"
    "    Content-Type: application/json\n"
    "\n"
    '    {"@type": "Document"}\n'
)


def test_builder_args(monkeypatch):
    html, warnings = build_builder_args(
        monkeypatch,
        "..  http:example:: curl echo\n"
        "    :builder-args:\n"
        "      echo:\n"
        "        method: createContent\n"
        "        timeout: 30\n"
        "        retry:\n"
        "          attempts: 3\n"
        "          backoff: 1.5\n" + REQUEST,
    )
    assert "builder-args" not in warnings
    assert "ERROR" not in warnings
    assert "echo method=createContent attempts=3" in html
    assert "http-example-curl" in html


def test_builder_args_example_block(monkeypatch):
    html, warnings = build_builder_args(
        monkeypatch,
        "..  http:example-block:: echo\n"
        "    :builder-args:\n"
        "      echo: {method: createContent, retry: {attempts: 3}}\n" + REQUEST,
    )
    assert "builder-args" not in warnings
    assert "ERROR" not in warnings
    assert "echo method=createContent attempts=3" in html


def test_builder_args_not_given(monkeypatch):
    html, warnings = build_builder_args(
        monkeypatch, "..  http:example:: curl echo\n" + REQUEST
    )
    assert "builder-args" not in warnings
    assert "ERROR" not in warnings
    assert "echo method=None attempts=None" in html


@pytest.mark.parametrize(
    "builder_args,error",
    (
        ("echo: [unclosed", "invalid YAML"),
        ("- echo", "expected a mapping of builder IDs to arguments"),
        ("", "builder arguments required"),
        ("wget: {}", "arguments for builders not used in this example: wget"),
        (
            "curl: {timeout: 30}",
            "Invalid :builder-args: for builder 'curl': "
            "got an unexpected keyword argument 'timeout'",
        ),
        (
            "echo: {metod: createContent}",
            "Invalid :builder-args: for builder 'echo': "
            "got an unexpected keyword argument 'metod'",
        ),
        (
            "echo: {request: 1}",
            "Invalid :builder-args: for builder 'echo': "
            "multiple values for argument 'request'",
        ),
        (
            "echo: createContent",
            "expected a mapping of argument names to values for builder 'echo'",
        ),
        (
            "echo: {1: createContent}",
            "Invalid :builder-args: for builder 'echo': keywords must be strings",
        ),
        (
            "{echo: {}, ECHO: {}}",
            "duplicate builder ID 'ECHO'",
        ),
        (
            "{1: {}}",
            "expected builder ID to be a string",
        ),
        (
            "{echo: {}, echo: {}}",
            "found duplicate key 'echo'",
        ),
        (
            "{echo: {method: a, method: b}}",
            "found duplicate key 'method'",
        ),
    ),
    ids=[
        "invalid-yaml",
        "not-mapping",
        "empty",
        "unknown-builder",
        "builtin",
        "unknown-argument",
        "request-argument",
        "not-mapping-arguments",
        "non-string-argument-name",
        "duplicate-builder",
        "non-string-builder-name",
        "exact-duplicate-builder",
        "duplicate-argument",
    ],
)
def test_builder_args_errors(monkeypatch, builder_args, error):
    html, warnings = build_builder_args(
        monkeypatch,
        "..  http:example:: curl echo\n"
        "    :builder-args: " + builder_args + "\n" + REQUEST,
    )
    assert error in warnings


MYST_REQUEST = (
    "POST /Plone/folder HTTP/1.1\n"
    "Host: localhost:8080\n"
    "Content-Type: application/json\n"
    "\n"
    '{"@type": "Document"}\n'
    "```\n"
)


@pytest.mark.parametrize(
    "options",
    (
        "---\n"
        "builder-args: |\n"
        "  echo:\n"
        "    method: createContent\n"
        "    retry:\n"
        "      attempts: 3\n"
        "---\n",
        ":builder-args: {echo: {method: createContent, retry: {attempts: 3}}}\n\n",
    ),
    ids=["yaml-block-scalar", "inline-mapping"],
)
def test_builder_args_myst(monkeypatch, options):
    html, warnings = build_builder_args(
        monkeypatch,
        "```{http:example} curl echo\n" + options + MYST_REQUEST,
        filename="index.md",
    )
    assert "builder-args" not in warnings
    assert "ERROR" not in warnings
    assert "echo method=createContent attempts=3" in html
    assert "http-example-curl" in html


@pytest.mark.parametrize(
    "directive,error",
    (
        (
            "..  http:example-block:: echo\n"
            "    :builder-args: {curl: {timeout: 30}}\n",
            "arguments for builders not used in this example: curl",
        ),
        (
            "..  http:example-block:: http\n"
            "    :builder-args: {echo: {method: createContent}}\n",
            "arguments for builders not used in this example: echo",
        ),
        (
            "..  http:example-block:: response\n"
            "    :builder-args: {echo: {method: createContent}}\n",
            "arguments for builders not used in this example: echo",
        ),
    ),
    ids=["example-block-unknown-builder", "http-block", "response-block"],
)
def test_builder_args_block_errors(monkeypatch, directive, error):
    html, warnings = build_builder_args(monkeypatch, directive + REQUEST)
    assert error in warnings


def test_builder_args_kwargs(monkeypatch):
    html, warnings = build_builder_args(
        monkeypatch,
        "..  http:example:: kwargs\n"
        "    :builder-args: {kwargs: {method: createContent, retry-count: 3}}\n"
        + REQUEST,
    )
    assert "builder-args" not in warnings
    assert "ERROR" not in warnings
    assert "kwargs method,retry-count" in html


def test_builder_args_empty_value(monkeypatch):
    html, warnings = build_builder_args(
        monkeypatch,
        "..  http:example:: curl echo\n    :builder-args: {echo: null}\n" + REQUEST,
    )
    assert "builder-args" not in warnings
    assert "ERROR" not in warnings
    assert "echo method=None attempts=None" in html


def test_builder_args_mixed_case(monkeypatch):
    # Builder ids are case-insensitive, like the directive arguments
    html, warnings = build_builder_args(
        monkeypatch,
        "..  http:example:: curl Echo\n"
        "    :builder-args: {ECHO: {method: createContent}}\n" + REQUEST,
    )
    assert "builder-args" not in warnings
    assert "ERROR" not in warnings
    assert "echo method=createContent attempts=None" in html


def test_invalid_request_file(monkeypatch):
    html, warnings = build_builder_args(
        monkeypatch,
        "..  http:example:: curl\n    :request: request.txt\n",
        files={"request.txt": "not a request\n"},
    )
    assert "Invalid HTTP request" in warnings


def test_builder_args_request_file(monkeypatch):
    html, warnings = build_builder_args(
        monkeypatch,
        "..  http:example:: curl echo\n"
        "    :request: request.txt\n"
        "    :builder-args: {echo: {method: createContent}}\n",
        files={"request.txt": REQUEST.replace("\n    ", "\n").lstrip()},
    )
    assert "builder-args" not in warnings
    assert "ERROR" not in warnings
    assert "echo method=createContent attempts=None" in html
    assert "http-example-curl" in html


def test_builder_args_blank_line(monkeypatch):
    # A blank line ends the option block, so the rest of the YAML becomes
    # request content, which is reported instead of crashing the build
    html, warnings = build_builder_args(
        monkeypatch,
        "..  http:example:: curl echo\n"
        "    :builder-args:\n"
        "      echo:\n"
        "        method: createContent\n"
        "\n"
        "        retry:\n"
        "          attempts: 3\n" + REQUEST,
    )
    assert "Invalid HTTP request" in warnings


def test_builder_args_signature_value_error(monkeypatch):
    import inspect

    def raise_value_error(func):
        raise ValueError("no signature found")

    monkeypatch.setattr(inspect, "signature", raise_value_error)
    html, warnings = build_builder_args(
        monkeypatch,
        "..  http:example:: echo\n"
        "    :builder-args: {echo: {method: createContent}}\n" + REQUEST,
    )
    assert "Invalid :builder-args: for builder 'echo': no signature found" in warnings


INVALID_JSON_REQUEST = (
    "\n"
    "    POST /Plone/folder HTTP/1.1\n"
    "    Host: localhost:8080\n"
    "    Content-Type: application/json\n"
    "\n"
    "    {not json\n"
)


@pytest.mark.parametrize("builder", ("curl", "requests"))
def test_invalid_json_body(monkeypatch, builder):
    html, warnings = build_builder_args(
        monkeypatch, "..  http:example:: {}\n".format(builder) + INVALID_JSON_REQUEST
    )
    assert "Invalid HTTP request: Expecting property name" in warnings


def test_builder_args_builder_failure(monkeypatch):
    html, warnings = build_builder_args(
        monkeypatch,
        "..  http:example:: echo\n    :builder-args: {echo: {retry: 5}}\n" + REQUEST,
    )
    assert (
        "Builder 'echo' failed: AttributeError: "
        "'int' object has no attribute 'get'" in warnings
    )


@pytest.mark.parametrize(
    "directive",
    ("..  http:example:: curl nosuch\n", "..  http:example-block:: nosuch\n"),
    ids=["example", "example-block"],
)
def test_unknown_builder(monkeypatch, directive):
    html, warnings = build_builder_args(monkeypatch, directive + REQUEST)
    assert '"nosuch" unknown; choose from "curl"' in warnings


def test_register_builder_mixed_case(monkeypatch):
    monkeypatch.setattr(
        directives, "AVAILABLE_BUILDERS", dict(directives.AVAILABLE_BUILDERS)
    )
    register_builder = directives.register_builder
    register_builder("MyClient", lambda request: "", "text", "My client")
    assert "myclient" in directives.AVAILABLE_BUILDERS
    assert directives.choose_builders(["MyClient"]) == ["myclient"]


@pytest.mark.parametrize("argument", ("HTTP", "Response"))
def test_example_block_mixed_case(monkeypatch, argument):
    html, warnings = build_builder_args(
        monkeypatch,
        "..  http:example-block:: {}\n".format(argument)
        + REQUEST
        + "\n\n    HTTP/1.1 201 Created\n",
    )
    assert "ERROR" not in warnings


def test_builder_args_blank_builder_id(monkeypatch):
    html, warnings = build_builder_args(
        monkeypatch,
        "..  http:example:: echo\n    :builder-args: {' ': {}}\n" + REQUEST,
    )
    assert "expected builder ID to be a string" in warnings


def test_builder_args_multiple_builders(monkeypatch):
    html, warnings = build_builder_args(
        monkeypatch,
        "..  http:example:: echo kwargs\n"
        "    :builder-args:\n"
        "      echo: {method: createContent}\n"
        "      kwargs: {retry: 3}\n" + REQUEST,
    )
    assert "builder-args" not in warnings
    assert "ERROR" not in warnings
    assert "echo method=createContent attempts=None" in html
    assert "kwargs retry" in html


def test_builder_args_comments(monkeypatch):
    html, warnings = build_builder_args(
        monkeypatch,
        "..  http:example:: echo\n"
        "    :builder-args:\n"
        "      # builder configuration\n"
        "      echo:\n"
        "        # method to call\n"
        "        method: createContent  # inline comment\n" + REQUEST,
    )
    assert "builder-args" not in warnings
    assert "ERROR" not in warnings
    assert "echo method=createContent attempts=None" in html


def test_builder_args_myst_block(monkeypatch):
    html, warnings = build_builder_args(
        monkeypatch,
        "```{http:example-block} echo\n"
        ":builder-args: {echo: {method: createContent, retry: {attempts: 3}}}\n\n"
        + MYST_REQUEST,
        filename="index.md",
    )
    assert "builder-args" not in warnings
    assert "ERROR" not in warnings
    assert "echo method=createContent attempts=3" in html
