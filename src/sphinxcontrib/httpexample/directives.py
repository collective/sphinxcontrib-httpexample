# -*- coding: utf-8 -*-
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.statemachine import StringList
from sphinx.directives.code import CodeBlock
from sphinxcontrib.httpexample import builders
from sphinxcontrib.httpexample import parsers
from sphinxcontrib.httpexample import utils

import os
import re


AVAILABLE_BUILDERS = {
    'curl': (builders.build_curl_command, 'bash'),
    'wget': (builders.build_wget_command, 'bash'),
    'httpie': (builders.build_httpie_command, 'bash'),
    'requests': (builders.build_requests_command, 'python'),
    'python-requests': (builders.build_requests_command, 'python'),
    'plone-javascript': (builders.build_plone_javascript_command, 'javascript'),
}

AVAILABLE_FIELDS = ['query']


def choose_builders(arguments):
    return [
        directives.choice(argument, AVAILABLE_BUILDERS)
        for argument in (arguments or [])
    ]


class HTTPExample(CodeBlock):

    required_arguments = 0
    optional_arguments = len(AVAILABLE_BUILDERS)

    option_spec = utils.merge_dicts(
        CodeBlock.option_spec,
        {
            'request': directives.unchanged,
            'response': directives.unchanged,
        },
    )

    @staticmethod
    def process_content(content):
        if content:
            raw = ('\r\n'.join(content)).encode('utf-8')
            request = parsers.parse_request(raw)
            params, _ = request.extract_fields('query')
            params = [(p[1], p[2]) for p in params]
            new_path = utils.add_url_params(request.path, params)
            content[0] = ' '.join([request.command, new_path, request.request_version])

        # split the request and optional response in the content.
        # The separator is two empty lines followed by a line starting with
        # 'HTTP/' or 'HTTP '
        request_content = StringList()
        request_content_no_fields = StringList()
        response_content = None
        emptylines_count = 0
        in_response = False
        is_field = r':({}) (.+): (.+)'.format('|'.join(AVAILABLE_FIELDS))
        for i, line in enumerate(content):
            source = content.source(i)
            if in_response:
                response_content.append(line, source)
            else:
                if emptylines_count >= 2 and (
                    line.startswith('HTTP/') or line.startswith('HTTP ')
                ):
                    in_response = True
                    response_content = StringList()
                    response_content.append(line, source)
                elif line == '':
                    emptylines_count += 1
                else:
                    request_content.extend(StringList([''] * emptylines_count, source))
                    request_content.append(line, source)

                    if not re.match(is_field, line):
                        request_content_no_fields.extend(
                            StringList([''] * emptylines_count, source)
                        )
                        request_content_no_fields.append(line, source)

                    emptylines_count = 0

        return (request_content, request_content_no_fields, response_content)

    def run(self):
        if self.content:
            processed = self.process_content(StringList(self.content))
            have_request = bool(processed[1])
            have_response = bool(processed[2])
        else:
            have_request = 'request' in self.options
            have_response = 'response' in self.options

        # Wrap and render main directive as 'http-example-http'
        klass = 'http-example-http'
        container = nodes.container('', classes=[klass])
        container.append(nodes.caption('', 'http'))
        block = HTTPExampleBlock(
            'http:example-block',
            ['http'],
            self.options,
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
                name = argument
                # Setting plone JavaScript tab name
                name = 'JavaScript' if name == 'plone-javascript' else name

                options = self.options.copy()
                options.pop('name', None)
                options.pop('caption', None)

                block = HTTPExampleBlock(
                    'http:example-block',
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
                klass = 'http-example-{}'.format(name)
                container = nodes.container('', classes=[klass])
                container.append(nodes.caption('', name))
                container.extend(block.run())

                # Append to result nodes
                result.append(container)

        # Append optional response
        if have_response:
            options = self.options.copy()
            options.pop('name', None)
            options.pop('caption', None)

            block = HTTPExampleBlock(
                'http:example-block',
                ['http'],
                options,
                self.content,
                self.lineno,
                self.content_offset,
                self.block_text,
                self.state,
                self.state_machine,
            )

            # Wrap and render main directive as 'http-example-response'
            klass = 'http-example-response'
            container = nodes.container('', classes=[klass])
            container.append(nodes.caption('', 'response'))
            container.extend(block.run())

            # Append to result nodes
            result.append(container)

        # Final wrap
        container_node = nodes.container('', classes=['http-example'])
        container_node.extend(result)

        return [container_node]


class HTTPExampleBlock(CodeBlock):
    required_arguments = 1

    option_spec = utils.merge_dicts(
        CodeBlock.option_spec,
        {
            'request': directives.unchanged,
            'response': directives.unchanged,
        },
    )

    def read_http_file(self, path):
        cwd = os.path.dirname(self.state.document.current_source)
        request = utils.resolve_path(path, cwd)
        with open(request) as fp:
            return StringList(list(map(str.rstrip, fp.readlines())), request)

    def run(self):
        if self.arguments == ['http']:
            if 'request' in self.options:
                self.content = self.read_http_file(self.options['request'])
            else:
                self.content = HTTPExample.process_content(self.content)[1]
        elif self.arguments == ['response']:
            if 'response' in self.options:
                self.content = self.read_http_file(self.options['response'])
            else:
                self.content = HTTPExample.process_content(self.content)[2]

            self.arguments = ['http']
        else:
            if 'request' in self.options:
                request_content_no_fields = self.read_http_file(self.options['request'])
            else:
                request_content_no_fields = HTTPExample.process_content(self.content)[1]

            raw = ('\r\n'.join(request_content_no_fields)).encode('utf-8')

            config = self.env.config
            request = parsers.parse_request(raw, config.httpexample_scheme)
            name = choose_builders(self.arguments)[0]
            builder_, language = AVAILABLE_BUILDERS[name]
            self.arguments = [language]

            command = builder_(request)
            self.content = StringList([command], request_content_no_fields.source(0))

        return super(HTTPExampleBlock, self).run()
