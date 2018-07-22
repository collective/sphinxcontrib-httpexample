# -*- coding: utf-8 -*-
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.statemachine import StringList
from sphinx.directives import CodeBlock
from sphinxcontrib.httpexample import builders
from sphinxcontrib.httpexample import parsers
from sphinxcontrib.httpexample import utils

import os


AVAILABLE_BUILDERS = {
    'curl': (builders.build_curl_command, 'bash'),
    'wget': (builders.build_wget_command, 'bash'),
    'httpie': (builders.build_httpie_command, 'bash'),
    'requests': (builders.build_requests_command, 'python'),
    'python-requests': (builders.build_requests_command, 'python')
}


def choose_builders(arguments):
    return [directives.choice(argument, AVAILABLE_BUILDERS)
            for argument in arguments]


class HTTPExample(CodeBlock):

    required_arguments = 0
    optional_arguments = len(AVAILABLE_BUILDERS)

    option_spec = utils.merge_dicts(CodeBlock.option_spec, {
        'request': directives.unchanged,
        'response': directives.unchanged,
    })

    def run(self):
        config = self.state.document.settings.env.config

        # Read enabled builders; Defaults to None
        if self.arguments:
            chosen_builders = choose_builders(self.arguments)
        else:
            chosen_builders = []

        # Enable 'http' language for http part
        self.arguments = ['http']

        # split the request and optional response in the content.
        # The separator is two empty lines followed by a line starting with
        # 'HTTP/'
        request_content = StringList()
        response_content = None
        emptylines_count = 0
        in_response = False
        for i, line in enumerate(self.content):
            source = self.content.source(i)
            if in_response:
                response_content.append(line, source)
            else:
                if emptylines_count >= 2 and line.startswith('HTTP/'):
                    in_response = True
                    response_content = StringList()
                    response_content.append(line, source)
                elif line == '':
                    emptylines_count += 1
                else:
                    request_content.extend(
                        StringList([''] * emptylines_count, source))
                    emptylines_count = 0
                    request_content.append(line, source)

        # Load optional external request
        cwd = os.path.dirname(self.state.document.current_source)
        if 'request' in self.options:
            request = utils.resolve_path(self.options['request'], cwd)
            with open(request) as fp:
                request_content = StringList(
                    list(map(str.rstrip, fp.readlines())), request)

        # Load optional external response
        if 'response' in self.options:
            response = utils.resolve_path(self.options['response'], cwd)
            with open(response) as fp:
                response_content = StringList(
                    list(map(str.rstrip, fp.readlines())), response)

        # reset the content to just the request
        self.content = request_content

        # Wrap and render main directive as 'http-example-http'
        klass = 'http-example-http'
        container = nodes.container('', classes=[klass])
        container.append(nodes.caption('', 'http'))
        container.extend(super(HTTPExample, self).run())

        # Init result node list
        result = [container]

        # Append builder responses
        for name in chosen_builders:
            raw = ('\r\n'.join(request_content)).encode('utf-8')
            request = parsers.parse_request(raw, config.httpexample_scheme)
            builder_, language = AVAILABLE_BUILDERS[name]
            command = builder_(request)

            content = StringList([command], request_content.source(0))
            options = self.options.copy()
            options.pop('name', None)
            options.pop('caption', None)

            block = CodeBlock(
                'code-block',
                [language],
                options,
                content,
                self.lineno,
                self.content_offset,
                self.block_text,
                self.state,
                self.state_machine
            )

            # Wrap and render main directive as 'http-example-{name}'
            klass = 'http-example-{}'.format(name)
            container = nodes.container('', classes=[klass])
            container.append(nodes.caption('', name))
            container.extend(block.run())

            # Append to result nodes
            result.append(container)

        # Append optional response
        if response_content:
            options = self.options.copy()
            options.pop('name', None)
            options.pop('caption', None)

            block = CodeBlock(
                'code-block',
                ['http'],
                options,
                response_content,
                self.lineno,
                self.content_offset,
                self.block_text,
                self.state,
                self.state_machine
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
