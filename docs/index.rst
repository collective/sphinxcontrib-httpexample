==============================================
Sphinx directive for RESTful HTTP API examples
==============================================

sphinxcontrib-httpexample is a Sphinx domain extension for describing RESTful HTTP APIs in detail.
It enhances `sphinxcontrib-httpdomain`_ with a simple call example directive.
The directive provided by this extension generates RESTful HTTP API call examples for different HTTP clients from a single HTTP request example.

The audience for this extension are developers and technical writers documenting their RESTful HTTP APIs.
This extension was originally developed for documenting `plone.restapi`_.

.. _sphinxcontrib-httpdomain: https://sphinxcontrib-httpdomain.readthedocs.io/en/stable/index.html
.. _plone.restapi: https://6.docs.plone.org/plone.restapi/docs/source/index.html


Configuration
=============
The URL scheme, either ``http`` or ``https``, used in the generated examples can be configured with the ``httpexample_scheme`` configuration variable.
It defaults to ``http``.

..  code-block:: python

    # conf.py
    httpexample_scheme = "https"


Syntax
======
There are two syntaxes, one each for inline and external sources.

The following example is of inline sources.

..  code-block:: rst

    ..  http:example:: space separated list of tools
        A required inline source of a raw plain text HTTP request example.
        This is required.


        An optional inline source of a raw plain text HTTP response example.
        If present, it must be separated from the request by two blank lines.
        It must begin with either ``HTTP/VERSION_NUMBER`` or ``HTTP ``.

The following example is of external sources.

..  code-block:: rst

    ..  http:example:: space separated list of tools
        :request: ../relative/path/to/plaintext/request/file
        :response: ../relative/path/to/plaintext/response/file

To display the response outside of the tabbed interface, then don't include it in the ``http:example`` directive, but instead list it separately.

For inline sources, use ``code-block`` with the ``http-response`` lexer.

..  code-block:: rst

    ..  http:example:: space separated list of tools
        A required inline source of a raw plain text HTTP request example.
        This is required.

    ..  code-block:: http
        An optional inline source of a raw plain text HTTP response example.

For external sources, use ``literalinclude`` with either the ``http`` or ``http-response`` lexer.

..  code-block:: rst

    ..  http:example:: space separated list of tools
        :request: ../relative/path/to/plaintext/request/file

    ..  literalinclude:: ../relative/path/to/plaintext/response/file
        :language: http


Example
=======

..  code-block:: rst

    ..  http:example:: curl wget httpie requests plone-client

        POST /Plone/folder HTTP/1.1
        Host: localhost:8080
        Accept: application/json
        Content-Type: application/json
        Authorization: Basic YWRtaW46YWRtaW4=


        HTTP 200 OK
        Content-Type: application/json

        {
            "@type": "Document",
            "title": "My Document"
        }


Rendering
=========

..  http:example:: curl wget httpie requests plone-client

    POST /Plone/folder HTTP/1.1
    Host: localhost:8080
    Accept: application/json
    Content-Type: application/json
    Authorization: Basic YWRtaW46YWRtaW4=


    HTTP 200 OK
    Content-Type: application/json

    {
        "@type": "Document",
        "title": "My Document"
    }


.. seealso::
    The :doc:`usage` provide an extensive demonstration of the capabilities of sphinxcontrib.httpexample.


Compatibility with other tab libraries
======================================

sphinxcontrib-httpexample is compatible with the following tab libraries.


`sphinx-inline-tabs <https://sphinx-inline-tabs.readthedocs.io/en/latest/>`_
----------------------------------------------------------------------------

..  tab:: http

    ..  http:example-block:: http
        :request: ../tests/fixtures/001.request.txt

..  tab:: curl

    ..  http:example-block:: curl
        :request: ../tests/fixtures/001.request.txt

..  tab:: wget

    ..  http:example-block:: wget
        :request: ../tests/fixtures/001.request.txt

..  tab:: httpie

    ..  http:example-block:: httpie
        :request: ../tests/fixtures/001.request.txt

..  tab:: requests

    ..  http:example-block:: wget
        :request: ../tests/fixtures/001.request.txt

..  tab:: response

    ..  http:example-block:: response
        :response: ../tests/fixtures/001.response.txt


`sphinx-design <https://sphinx-design.readthedocs.io/en/furo-theme/tabs.html>`_
-------------------------------------------------------------------------------

..  tab-set::

    ..  tab-item:: http

        ..  http:example-block:: http
            :request: ../tests/fixtures/001.request.txt

    ..  tab-item:: curl

        ..  http:example-block:: curl
            :request: ../tests/fixtures/001.request.txt

    ..  tab-item:: wget

        ..  http:example-block:: wget
            :request: ../tests/fixtures/001.request.txt

    ..  tab-item:: httpie

        ..  http:example-block:: httpie
            :request: ../tests/fixtures/001.request.txt

    ..  tab-item:: requests

        ..  http:example-block:: wget
            :request: ../tests/fixtures/001.request.txt

    ..  tab-item:: response

        ..  http:example-block:: response
            :response: ../tests/fixtures/001.response.txt


Custom builders
===============

sphinxcontrib.httpexample supports custom builders.

See the `issue tracker <https://github.com/collective/sphinxcontrib-httpexample/issues>`_ to request or provide a custom builder.

.. seealso::
    See an example :doc:`custom` for the `@plone/client <https://www.npmjs.com/package/@plone/client>`_ package, an agnostic library that provides easy access to the Plone REST API from a client written in TypeScript.


Supported tools
===============

-   curl_
-   wget_
-   httpie_
-   requests_

.. _curl: https://curl.haxx.se/
.. _wget: https://www.gnu.org/software/wget/
.. _httpie: https://httpie.org/
.. _requests: https://requests.readthedocs.io/en/stable/


Contents
========
..  toctree::
    :maxdepth: 2

    usage
    custom
