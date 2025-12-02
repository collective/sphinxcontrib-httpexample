from sphinxcontrib.httpexample import HTTPRequest
from urllib.parse import parse_qs
from urllib.parse import urlparse
import json
import re


def is_valid_js_identifier(key):
    return re.match(r"^[_a-zA-Z][_a-zA-Z0-9]*$", key)


def python_to_js_literal(value, indent=0):
    indent_str = "  " * indent
    next_indent_str = "  " * (indent + 1)

    if isinstance(value, dict):
        lines = ["{"]
        for k, v in value.items():
            key = k if is_valid_js_identifier(k) else f"'{k}'"
            js_val = python_to_js_literal(v, indent + 1)
            lines.append(f"{next_indent_str}{key}: {js_val},")
        lines.append(f"{indent_str}}}")
        return "\n".join(lines)

    elif isinstance(value, list):
        if not value:
            return "[]"
        items = [f"{python_to_js_literal(item, indent + 1)}," for item in value]
        return (
            "[\n"
            + "\n".join(f"{next_indent_str}{item}" for item in items)
            + f"\n{indent_str}]"
        )

    elif isinstance(value, str):
        return f"'{value}'"

    elif isinstance(value, bool):
        return "true" if value else "false"

    elif value is None:
        return "null"

    else:
        return str(value)


def get_content(request: HTTPRequest):
    url = urlparse(request.url())
    path = f'/{url.path.split("/", 2)[-1]}'
    qs = parse_qs(url.query)
    payload = {
        "path": path,
    }
    if qs.get("expand"):
        payload["expanders"] = qs.get("expand", [])[0].split(",")
    return f"""\
const {{ data, status }} = cli.getContent({python_to_js_literal(payload)});
"""


def patch_content(request: HTTPRequest):
    url = urlparse(request.url())
    path = f'/{url.path.split("/", 2)[-1]}'
    payload = {
        "path": path,
        "data": request.data(),
    }
    return f"""\
cli.updateContent({python_to_js_literal(payload)});
"""


def build_plone_javascript_command(request: HTTPRequest):
    url = urlparse(request.url())
    portal_path = url.path.split("/")[1]
    output = f"""\
import PloneClient from '@plone/client';

const cli = PloneClient.initialize({{apiPath: '{url.scheme}://{url.netloc}/{portal_path}'}});

"""
    auth = request.auth()
    if auth[-1]:
        username, password = auth[-1].split(":")
        output += f"""\
cli.login({{username: '{username}', password: '{password}'}});

"""
    if request.command == "GET":
        return output + get_content(request)
    elif request.command == "PATCH":
        return output + patch_content(request)
    return output
