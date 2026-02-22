# -*- coding: utf-8 -*-
"""A custom Pygments lexer for HTTP responses."""

from pygments.lexer import bygroups
from pygments.lexer import Lexer
from pygments.lexer import RegexLexer
from pygments.lexers import get_lexer_for_mimetype
from pygments.lexers import TextLexer
from pygments.token import Name
from pygments.token import String
from pygments.token import Text
from pygments.token import Token
import re


class HTTPHeaderLexer(RegexLexer):
    """A simple lexer for HTTP headers."""

    name = "HTTPHeader"
    tokens = {
        "root": [
            (
                r"^([a-zA-Z][a-zA-Z0-9-]*)(:\s*)(.*)",
                bygroups(Name.Attribute, Text, String),
            ),
            (r".+", Text),
        ]
    }


class HTTPResponseLexer(Lexer):
    """
    A custom Pygments lexer that delegates the body parsing to another lexer
    based on the Content-Type header.
    """

    name = "HTTPResponse"
    aliases = ["http-response"]

    def get_tokens_unprocessed(self, text, **options):
        # 1. Split headers and body
        parts = re.split(r"(\r?\n\r?\n)", text, maxsplit=1)
        header_part = parts[0]

        # 2. Handle the Status Line to avoid Token.Error
        # Supports: "HTTP 200 OK", "HTTP/1.1 200 OK", "HTTP/2 200"
        lines = header_part.splitlines(keepends=True)
        if lines:
            status_line = lines[0]
            if status_line.startswith("HTTP"):
                yield 0, Token.Keyword.Reserved, status_line.rstrip()
                if status_line.endswith("\n") or status_line.endswith("\r\n"):
                    yield len(status_line.rstrip()), Token.Text, status_line[
                        len(status_line.rstrip()) :
                    ]
                header_remainder = "".join(lines[1:])
            else:
                header_remainder = header_part
        else:
            header_remainder = ""

        # 3. Parse remaining headers
        h_lexer = HTTPHeaderLexer()
        current_offset = len(lines[0]) if lines and lines[0].startswith("HTTP") else 0
        for line in header_remainder.splitlines(keepends=True):
            for pos, token, value in h_lexer.get_tokens_unprocessed(line):
                yield current_offset + pos, token, value
            current_offset += len(line)

        if len(parts) < 3:
            return

        # 4. Yield the separator
        separator = parts[1]
        body_part = parts[2]
        yield len(header_part), Token.Text, separator

        # 5. Delegate body parsing
        ct_match = re.search(
            r"^Content-Type:\s*([^;\n\r\s]+)", header_part, re.I | re.M
        )
        mime = ct_match.group(1).strip() if ct_match else "text/plain"
        try:
            body_lexer = get_lexer_for_mimetype(mime)
        except Exception:
            body_lexer = TextLexer()

        body_offset = len(header_part) + len(separator)
        for pos, token, value in body_lexer.get_tokens_unprocessed(
            body_part, **options
        ):
            yield body_offset + pos, token, value
