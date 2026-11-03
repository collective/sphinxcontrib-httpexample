==============
Custom builder
==============

Some packages use an API to send HTTP requests.
This allows developers to focus on API calls instead of forming HTTP requests with low level utilities.
For such packages, sphinxcontrib.httpexample supports custom builders.

The examples in this chapter use the `@plone/client <https://www.npmjs.com/package/@plone/client>`_ package, an agnostic library that provides easy access to the Plone REST API from a client written in TypeScript.


Register
========

Create a file at :file:`docs/plone_client.py`.

In this file, define a custom method as your builder.

.. code:: python

    def build_plone_client_command(request: HTTPRequest) -> str:
        output = ""
        # ...
        return output

Next, in :file:`docs/conf.py`, register the builder with ``register_builder()`` to make it available.

.. code:: python

    from plone_client import build_plone_client_command
    from sphinxcontrib.httpexample import register_builder

    register_builder(
        # Name of the builder used in the directive
        "plone-client",
        # Function that builds the command
        build_plone_client_command,
        # Language for syntax highlighting
        "javascript",
        # Display name for the documentation tab
        "@plone/client"
    )

The ``register_builder`` method has the following parameters.

``name``
    The name of the builder to use in the reStructuredText or MyST directive.

``builder``
    The function that builds the command to send an HTTP request.

``language``
    The language, or lexer, to use for syntax highlighting.

``label``
    The display name of the tab in the documentation.

For a complete example, download :download:`plone_client.py`.


Builder arguments
=================

Use the ``:builder-args:`` option of ``http:example`` or ``http:example-block`` to pass extra arguments to custom builders.
Its value is parsed as YAML.
The root keys are the builder IDs given as the directive arguments, and like them, are case-insensitive.
Each value is a mapping of argument names to values, which are passed to that builder as keyword arguments.
An empty value for a builder (such as ``null`` or ``{}``) passes no arguments.
In reStructuredText, the YAML must not contain blank lines, because a blank line ends the directive options.

..  code-block:: rst

    ..  http:example:: curl my-client
        :builder-args:
          my-client:
            client_method: createContent

        POST /Plone/folder HTTP/1.1
        Host: localhost:8080
        Content-Type: application/json

        {
            "@type": "Document",
            "title": "My New Document"
        }

A builder accepts arguments by declaring them as keyword parameters with default values.
It is called with only the request when the example has no arguments for it, so builders without keyword parameters keep working.

..  code-block:: python

    def build_my_client_command(request, client_method):
        ...

Argument keys are not normalized (for example, dashes are not converted to underscores) and must match the builder function's parameter names.
To accept any arguments, including names that are not valid Python identifiers, use ``**kwargs``.

Values are parsed as YAML 1.1 with PyYAML, so quote values such as ``yes``, ``on``, or ``0123`` to pass them as strings.

In MyST Markdown, nested option values must be given either as a block scalar in a YAML options block, or as an inline YAML mapping.
MyST does not keep the indentation of nested mappings in directive options.

..  code-block:: markdown
    :caption: Option values as a block scalar in a YAML options block.

    ```{http:example} curl my-client
    ---
    builder-args: |
      my-client:
        client_method: createContent
    ---
    POST /Plone/folder HTTP/1.1
    Host: localhost:8080
    ```

..  code-block:: markdown
    :caption: Option values as an inline YAML mapping.

    ```{http:example} curl my-client
    :builder-args: {my-client: {client_method: createContent}}

    POST /Plone/folder HTTP/1.1
    Host: localhost:8080
    ```

The build reports an error if the option is empty, if the YAML is invalid, if it is not a mapping of builder IDs to mappings of arguments, if it has duplicate builder IDs or argument names, if it has arguments for a builder not listed in the example, or if the builder does not accept the given arguments.
The built-in builders do not accept arguments.


Create content
==============

The following example creates content at the specified path with the given JSON body.

..  http:example:: curl plone-client

    POST /Plone/folder HTTP/1.1
    Host: localhost:8080
    Content-Type: application/json
    Accept: application/json
    Authorization: Basic YWRtaW46YWRtaW4=

    {
        "@type": "Document",
        "title": "My New Document"
    }


Get content
===========

The following example gets the content at the specified location.

..  http:example:: curl plone-client

    GET /Plone/folder/my-document HTTP/1.1
    Host: localhost:8080
    Accept: application/json

The following example gets the content at the specified location, using an expansion.

..  http:example:: curl plone-client

    GET /Plone/folder/my-document?expand=breadcrumbs,navigation HTTP/1.1
    Host: localhost:8080
    Accept: application/json
    Authorization: Basic YWRtaW46c2VjcmV0


Update content
==============

The following example updates the content at the specified location.

..  http:example:: curl plone-client

    PATCH /Plone/folder/my-document HTTP/1.1
    Host: localhost:8080
    Content-Type: application/json
    Accept: application/json
    Authorization: Basic YWRtaW46YWRtaW4=

    {
        "title": "My New Document Title"
    }
