# -*- coding: utf-8 -*-
from docutils.nodes import container
from docutils.statemachine import StringList
from sphinx.directives import CodeBlock
from docutils.parsers.rst import directives
from sphinxcontrib.httpexample import builders
from sphinxcontrib.httpexample import parsers

AVAILABLE_BUILDERS = {
    'curl': (builders.build_curl_command, 'bash'),
    'httpie': (builders.build_httpie_command, 'bash'),
    'requests': (builders.build_requests_command, 'python')
}


def choose_builders(arguments):
    return [directives.choice(argument, AVAILABLE_BUILDERS)
            for argument in arguments]


class HTTPExample(CodeBlock):

    required_arguments = 0
    optional_arguments = len(AVAILABLE_BUILDERS)

    def run(self):
        if self.arguments:
            chosen_builders = choose_builders(self.arguments)
        else:
            chosen_builders = []

        self.arguments = ['http']
        if 'caption' not in self.options:
            self.options['caption'] = 'http'
        nodes = super(HTTPExample, self).run()

        for name in chosen_builders:
            raw = ('\r\n'.join(self.content)).encode('utf-8')
            request = parsers.parse_request(raw)
            builder_, language = AVAILABLE_BUILDERS[name]
            command = builder_(request)

            block_text = '.. code-block::\n\n   {}'.format(language)
            content = StringList([command], self.content.source(0))
            options = self.options.copy()
            options.pop('caption', None)
            options.pop('name', None)
            options['caption'] = name

            block = CodeBlock(
                'code-block',
                [language],
                options,
                content,
                self.lineno,
                self.content_offset,
                block_text,
                self.state,
                self.state_machine
            )
            nodes.extend(block.run())

        container_node = container('', literal_block=True,
                                   classes=['http-example'])
        container_node.extend(nodes)
        return [container_node]
