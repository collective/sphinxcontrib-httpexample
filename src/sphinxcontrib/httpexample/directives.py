# -*- coding: utf-8 -*-
from docutils import nodes
from docutils.statemachine import StringList
from sphinx.directives import CodeBlock
from docutils.parsers.rst import directives
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
        # Read enabled builders; Defaults to None
        if self.arguments:
            chosen_builders = choose_builders(self.arguments)
        else:
            chosen_builders = []

        # Enable 'http' language for http part
        self.arguments = ['http']

        # Optionally, read directive content from 'request' option
        cwd = os.path.dirname(self.state.document.current_source)
        if 'request' in self.options:
            request = utils.resolve_path(self.options['request'], cwd)
            with open(request) as fp:
                self.content = StringList(
                    list(map(str.rstrip, fp.readlines())), request)

        # Wrap and render main directive as 'http-example-http'
        klass = 'http-example-http'
        container = nodes.container('', classes=[klass])
        container.append(nodes.caption('', 'http'))
        container.extend(super(HTTPExample, self).run())

        # Init result node list
        result = [container]

        # Append builder responses
        for name in chosen_builders:
            raw = ('\r\n'.join(self.content)).encode('utf-8')
            request = parsers.parse_request(raw)
            builder_, language = AVAILABLE_BUILDERS[name]
            command = builder_(request)

            content = StringList([command], self.content.source(0))
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
        if 'response' in self.options:
            response = utils.resolve_path(self.options['response'], cwd)
            with open(response) as fp:
                content = StringList(
                    list(map(str.rstrip, fp.readlines())), response)

            options = self.options.copy()
            options.pop('name', None)
            options.pop('caption', None)

            block = CodeBlock(
                'code-block',
                ['http'],
                options,
                content,
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
