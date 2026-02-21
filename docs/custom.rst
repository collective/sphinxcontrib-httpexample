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
