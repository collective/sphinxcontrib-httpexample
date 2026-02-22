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

http_responses = []
http_formats = ["HTTP ", "HTTP/1.1 ", "HTTP/2.0 "]
for http_format in http_formats:
    offset = len(http_format)
    http_responses.append(
        (f"{http_format}204 No Content",
            [
                (0, Token.Keyword.Reserved, f"{http_format}204 No Content"),
            ]
        )
    )
    http_responses.append(
        (f"{http_format}200 OK\n" "Content-Type: application/json",
            [
                (0, Token.Keyword.Reserved, f"{http_format}200 OK"),
                (6 + offset, Token.Text, "\n"),
                (7 + offset, Name.Attribute, "Content-Type"),
                (19 + offset, Text, ": "),
                (21 + offset, String, "application/json"),
            ],
        )
    )
    http_responses.append(
        (f"{http_format}200 OK\n"
        "Content-Type: application/json\n"
        "\n"
        '{"foo": "bar"}',
            [
                (0, Token.Keyword.Reserved, f"{http_format}200 OK"),
                (6 + offset, Token.Text, "\n"),
                (7 + offset, Name.Attribute, "Content-Type"),
                (19 + offset, Text, ": "),
                (21 + offset, String, "application/json"),
                (37 + offset, Token.Text, "\n\n"),
                (39 + offset, Token.Punctuation, "{"),
                (40 + offset, Token.Name.Tag, '"foo"'),
                (45 + offset, Token.Punctuation, ":"),
                (46 + offset, Token.Text.Whitespace, " "),
                (47 + offset, Token.Literal.String.Double, '"bar"'),
                (52 + offset, Token.Punctuation, "}"),
            ],
        )
    )
    http_responses.append(
        (
            f"{http_format}200 OK\n"
            "Content-Type: application/json\n"
            "Content-Length: 15\n"
            "\n"
            '{"foo": "bar"}',
            [
                (0, Token.Keyword.Reserved, f"{http_format}200 OK"),
                (6 + offset, Token.Text, "\n"),
                (7 + offset, Name.Attribute, "Content-Type"),
                (19 + offset, Text, ": "),
                (21 + offset, String, "application/json"),
                (37 + offset, Token.Text.Whitespace, "\n"),
                (38 + offset, Name.Attribute, "Content-Length"),
                (52 + offset, Text, ": "),
                (54 + offset, String, "15"),
                (56 + offset, Token.Text, "\n\n"),
                (58 + offset, Token.Punctuation, "{"),
                (59 + offset, Token.Name.Tag, '"foo"'),
                (64 + offset, Token.Punctuation, ":"),
                (65 + offset, Token.Text.Whitespace, " "),
                (66 + offset, Token.Literal.String.Double, '"bar"'),
                (71 + offset, Token.Punctuation, "}"),
            ],
        )
    )
    http_responses.append(
        (
        f"{http_format}200 OK\n" "Content-Type: application/unknown\n" "\n" "foo",
            [
                (0, Token.Keyword.Reserved, f"{http_format}200 OK"),
                (6 + offset, Token.Text, "\n"),
                (7 + offset, Name.Attribute, "Content-Type"),
                (19 + offset, Text, ": "),
                (21 + offset, String, "application/unknown"),
                (40 + offset, Token.Text, "\n\n"),
                (42 + offset, Token.Text, "foo"),
            ],
        ),
    )
    http_responses.append(
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
        )
    )

@pytest.mark.parametrize("text,expected", http_responses)
def test_response_lexing(lexer, text, expected):
    """Parametrized tests for various HTTP response lexing scenarios."""
    assert list(lexer.get_tokens_unprocessed(text)) == expected
