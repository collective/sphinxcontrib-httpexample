# -*- coding: utf-8 -*-
"""Tests for sphinxcontrib-httpexample."""

from pygments.token import Keyword
from pygments.token import Name
from pygments.token import String
from pygments.token import Text
from pygments.token import Token
from sphinxcontrib.httpexample.lexers import HTTPResponseLexer
import pytest


@pytest.fixture
def lexer():
    """Return a new HTTPResponseLexer instance for each test."""
    return HTTPResponseLexer()


@pytest.mark.parametrize(
    "text,expected",
    [
        (
            "HTTP/1.1 204 No Content",
            [
                (0, Token.Keyword.Reserved, "HTTP/1.1 204 No Content"),
            ],
        ),
        (
            "HTTP/1.1 200 OK\n" "Content-Type: application/json",
            [
                (0, Token.Keyword.Reserved, "HTTP/1.1 200 OK"),
                (15, Token.Text, "\n"),
                (16, Name.Attribute, "Content-Type"),
                (28, Text, ": "),
                (30, String, "application/json"),
            ],
        ),
        (
            "HTTP/1.1 200 OK\n"
            "Content-Type: application/json\n"
            "\n"
            '{"foo": "bar"}',
            [
                (0, Token.Keyword.Reserved, "HTTP/1.1 200 OK"),
                (15, Token.Text, "\n"),
                (16, Name.Attribute, "Content-Type"),
                (28, Text, ": "),
                (30, String, "application/json"),
                (46, Token.Text, "\n\n"),
                (48, Token.Punctuation, "{"),
                (49, Token.Name.Tag, '"foo"'),
                (54, Token.Punctuation, ":"),
                (55, Token.Text.Whitespace, " "),
                (56, Token.Literal.String.Double, '"bar"'),
                (61, Token.Punctuation, "}"),
            ],
        ),
        (
            (
                "HTTP/1.1 200 OK\n"
                "Content-Type: application/json\n"
                "Content-Length: 15\n"
                "\n"
                '{"foo": "bar"}'
            ),
            [
                (0, Token.Keyword.Reserved, "HTTP/1.1 200 OK"),
                (15, Token.Text, "\n"),
                (16, Name.Attribute, "Content-Type"),
                (28, Text, ": "),
                (30, String, "application/json"),
                (46, Token.Text.Whitespace, "\n"),
                (47, Name.Attribute, "Content-Length"),
                (61, Text, ": "),
                (63, String, "15"),
                (65, Token.Text, "\n\n"),
                (67, Token.Punctuation, "{"),
                (68, Token.Name.Tag, '"foo"'),
                (73, Token.Punctuation, ":"),
                (74, Token.Text.Whitespace, " "),
                (75, Token.Literal.String.Double, '"bar"'),
                (80, Token.Punctuation, "}"),
            ],
        ),
        (
            "HTTP/1.1 200 OK\n" "Content-Type: application/unknown\n" "\n" "foo",
            [
                (0, Token.Keyword.Reserved, "HTTP/1.1 200 OK"),
                (15, Token.Text, "\n"),
                (16, Name.Attribute, "Content-Type"),
                (28, Text, ": "),
                (30, String, "application/unknown"),
                (49, Token.Text, "\n\n"),
                (51, Token.Text, "foo"),
            ],
        ),
        (
            "Content-Type: application/json\n" "\n" '{"foo": "bar"}',
            [
                (0, Name.Attribute, "Content-Type"),
                (12, Text, ": "),
                (14, String, "application/json"),
                (30, Token.Text, "\n\n"),
                (32, Token.Punctuation, "{"),
                (33, Token.Name.Tag, '"foo"'),
                (38, Token.Punctuation, ":"),
                (39, Token.Text.Whitespace, " "),
                (40, Token.Literal.String.Double, '"bar"'),
                (45, Token.Punctuation, "}"),
            ],
        ),
    ],
)
def test_response_lexing(lexer, text, expected):
    """Parametrized tests for various HTTP response lexing scenarios."""
    assert list(lexer.get_tokens_unprocessed(text)) == expected
