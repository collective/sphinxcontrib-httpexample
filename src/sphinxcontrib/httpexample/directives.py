# -*- coding: utf-8 -*-
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.statemachine import StringList
from sphinx.directives.code import CodeBlock
from sphinxcontrib.httpexample import builders
from sphinxcontrib.httpexample import parsers
from sphinxcontrib.httpexample import utils
import inspect
import os
import re
import yaml


AVAILABLE_BUILDERS = {
    "curl": (builders.build_curl_command, "shell"),
    "wget": (builders.build_wget_command, "shell"),
    "httpie": (builders.build_httpie_command, "shell"),
    "python-requests": (builders.build_requests_command, "python"),
    "requests": (builders.build_requests_command, "python"),
}

AVAILABLE_FIELDS = ["query"]


def choose_builders(arguments):
    return [
        directives.choice(argument, tuple(AVAILABLE_BUILDERS))
        for argument in (arguments or [])
    ]


def builder_id(name):
    """Normalize a builder ID like directives.choice does for arguments."""
    return name.lower().strip() if isinstance(name, str) else name


class UniqueKeyLoader(yaml.SafeLoader):
    """SafeLoader that rejects duplicate mapping keys instead of keeping the last."""

    def construct_mapping(self, node, deep=False):
        keys = []
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in keys:
                raise yaml.constructor.ConstructorError(
                    None,
                    None,
                    "found duplicate key '{}'".format(key),
                    key_node.start_mark,
                )
            keys.append(key)
        return super().construct_mapping(node, deep=deep)


def builder_args(argument):
    """Parse the :builder-args: option as a YAML mapping of builder IDs."""
    if not argument or not argument.strip():
        raise ValueError("builder arguments required")
    try:
        value = yaml.load(argument, Loader=UniqueKeyLoader)
    except yaml.YAMLError as e:
        raise ValueError("invalid YAML: {}".format(e))
    if not isinstance(value, dict):
        raise ValueError("expected a mapping of builder IDs to arguments")
    result = {}
    for name, kwargs in value.items():
        if not isinstance(name, str) or not name.strip():
            raise ValueError("expected builder ID to be a string")
        bid = builder_id(name)
        if bid in result:
            raise ValueError("duplicate builder ID '{}'".format(name))
        if kwargs is None:
            kwargs = {}
        elif not isinstance(kwargs, dict):
            raise ValueError(
                "expected a mapping of argument names to values "
                "for builder '{}'".format(name)
            )
        result[bid] = kwargs
    return result


def check_builder_args(directive, names):
    unknown = set(directive.options.get("builder-args", {})) - set(names)
    if unknown:
        raise directive.error(
            ":builder-args: has arguments for builders not used in "
            "this example: {}".format(", ".join(sorted(map(str, unknown))))
        )


def process_content_or_error(directive, content):
    try:
        return HTTPExample.process_content(content)
    except Exception as e:
        raise directive.error("Invalid HTTP request: {}".format(e))


def call_builder(directive, name, builder, request, kwargs):
    """Call the builder, reporting invalid :builder-args: as an error."""
    if kwargs:
        error = "Invalid :builder-args: for builder '{}': {}"
        try:
            inspect.signature(builder).bind(request, **kwargs)
        except (TypeError, ValueError) as e:
            raise directive.error(error.format(name, e))
    try:
        return builder(request, **kwargs)
    except Exception as e:
        # e.g. an argument value of an unexpected type
        raise directive.error(
            "Builder '{}' failed: {}: {}".format(name, type(e).__name__, e)
        )


def register_builder(name, builder, language, label):
    AVAILABLE_BUILDERS[builder_id(name)] = (builder, language, label)


class HTTPExample(CodeBlock):

    required_arguments = 0
    optional_arguments = len(AVAILABLE_BUILDERS)

    option_spec = utils.merge_dicts(
        CodeBlock.option_spec,
        {
            "request": directives.unchanged,
            "response": directives.unchanged,
            "builder-args": builder_args,
        },
    )

    @staticmethod
    def process_content(content):
        if content:
            raw = ("\r\n".join(content)).encode("utf-8")
            request = parsers.parse_request(raw)
            params, _ = request.extract_fields("query")
            params = [(p[1], p[2]) for p in params]
            new_path = utils.add_url_params(request.path, params)
            content[0] = " ".join([request.command, new_path, request.request_version])

        # split the request and optional response in the content.
        # The separator is two empty lines followed by a line starting with
        # 'HTTP/' or 'HTTP '
        request_content = StringList()
        request_content_no_fields = StringList()
        response_content = None
        emptylines_count = 0
        in_response = False
        is_field = r":({}) (.+): (.+)".format("|".join(AVAILABLE_FIELDS))
        for i, line in enumerate(content):
            source = content.source(i)
            if in_response:
                response_content.append(line, source)
            else:
                if emptylines_count >= 2 and (
                    line.startswith("HTTP/") or line.startswith("HTTP ")
                ):
                    in_response = True
                    response_content = StringList()
                    response_content.append(line, source)
                elif line == "":
                    emptylines_count += 1
                else:
                    request_content.extend(StringList([""] * emptylines_count, source))
                    request_content.append(line, source)

                    if not re.match(is_field, line):
                        request_content_no_fields.extend(
                            StringList([""] * emptylines_count, source)
                        )
                        request_content_no_fields.append(line, source)

                    emptylines_count = 0

        return (request_content, request_content_no_fields, response_content)

    def run(self):
        try:
            choose_builders(self.arguments)
        except ValueError as e:
            raise self.error(str(e))
        check_builder_args(self, [builder_id(arg) for arg in self.arguments])

        if self.content:
            processed = process_content_or_error(self, StringList(self.content))
            have_request = bool(processed[1])
            have_response = bool(processed[2])
        else:
            have_request = "request" in self.options
            have_response = "response" in self.options

        # Wrap and render main directive as 'http-example-http'
        klass = "http-example-http"
        container = nodes.container("", classes=[klass])
        container.append(nodes.caption("", "http"))
        options = self.options.copy()
        options.pop("builder-args", None)
        block = HTTPExampleBlock(
            "http:example-block",
            ["http"],
            options,
            self.content,
            self.lineno,
            self.content_offset,
            self.block_text,
            self.state,
            self.state_machine,
        )
        container.extend(block.run())

        # Init result node list
        result = [container]

        # Append builder responses
        if have_request:
            for argument in self.arguments:
                name = builder_id(argument)
                builder_entry = AVAILABLE_BUILDERS.get(name)
                if builder_entry is not None and len(builder_entry) == 3:
                    label = builder_entry[2]
                else:
                    label = argument
                options = self.options.copy()
                options.pop("name", None)
                options.pop("caption", None)
                if name in options.get("builder-args", {}):
                    options["builder-args"] = {name: options["builder-args"][name]}
                else:
                    options.pop("builder-args", None)

                block = HTTPExampleBlock(
                    "http:example-block",
                    [argument],
                    options,
                    self.content,
                    self.lineno,
                    self.content_offset,
                    self.block_text,
                    self.state,
                    self.state_machine,
                )

                # Wrap and render main directive as 'http-example-{name}'
                klass = "http-example-{}".format(argument)
                container = nodes.container("", classes=[klass])
                container.append(nodes.caption("", label))
                container.extend(block.run())

                # Append to result nodes
                result.append(container)

        # Append optional response
        if have_response:
            options = self.options.copy()
            options.pop("name", None)
            options.pop("caption", None)
            options.pop("builder-args", None)

            block = HTTPExampleBlock(
                "http:example-block",
                ["response"],
                options,
                self.content,
                self.lineno,
                self.content_offset,
                self.block_text,
                self.state,
                self.state_machine,
            )

            # Wrap and render main directive as 'http-example-response'
            klass = "http-example-response"
            container = nodes.container("", classes=[klass])
            container.append(nodes.caption("", "response"))
            container.extend(block.run())

            # Append to result nodes
            result.append(container)

        # Final wrap
        container_node = nodes.container("", classes=["http-example"])
        container_node.extend(result)

        return [container_node]


class HTTPExampleBlock(CodeBlock):
    required_arguments = 1

    option_spec = utils.merge_dicts(
        CodeBlock.option_spec,
        {
            "request": directives.unchanged,
            "response": directives.unchanged,
            "builder-args": builder_args,
        },
    )

    def read_http_file(self, path):
        cwd = os.path.dirname(self.state.document.current_source)
        request = utils.resolve_path(path, cwd)
        with open(request) as fp:
            return StringList(list(map(str.rstrip, fp.readlines())), request)

    def run(self):
        arg = builder_id(self.arguments[0]) if self.arguments else ""
        if arg in ("http", "response"):
            check_builder_args(self, [])

        if arg == "http":
            if "request" in self.options:
                self.content = self.read_http_file(self.options["request"])
            else:
                self.content = process_content_or_error(self, self.content)[1]
            self.arguments = ["http"]
        elif arg == "response":
            if "response" in self.options:
                self.content = self.read_http_file(self.options["response"])
            else:
                self.content = process_content_or_error(self, self.content)[2]
            self.arguments = ["http-response"]
        else:
            try:
                name = choose_builders(self.arguments)[0]
            except ValueError as e:
                raise self.error(str(e))
            check_builder_args(self, [name])
            try:
                builder_, language, _ = AVAILABLE_BUILDERS[name]
            except ValueError:
                builder_, language = AVAILABLE_BUILDERS[name]

            if "request" in self.options:
                request_content_no_fields = self.read_http_file(self.options["request"])
            else:
                request_content_no_fields = process_content_or_error(
                    self, self.content
                )[1]

            raw = ("\r\n".join(request_content_no_fields)).encode("utf-8")

            config = self.env.config
            try:
                request = parsers.parse_request(raw, config.httpexample_scheme)
                # builders parse the body lazily, so validate it here
                request.data()
            except Exception as e:
                raise self.error("Invalid HTTP request: {}".format(e))
            self.arguments = [language]

            kwargs = self.options.get("builder-args", {}).get(name, {})
            command = call_builder(self, name, builder_, request, kwargs)
            self.content = StringList([command], request_content_no_fields.source(0))

        return super(HTTPExampleBlock, self).run()
