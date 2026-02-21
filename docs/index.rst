==============================================
Sphinx directive for RESTful HTTP API examples
==============================================

sphinxcontrib-httpexample is a Sphinx domain extension for describing RESTful HTTP APIs in detail.
It enhances `sphinxcontrib-httpdomain`_ with a simple call example directive.
The directive provided by this extension generates RESTful HTTP API call examples for different tools from a single HTTP request example.

The audience for this extension are developers and technical writers documenting their RESTful HTTP APIs.
This extension was originally developed for documenting `plone.restapi`_.

.. _sphinxcontrib-httpdomain: https://pythonhosted.org/sphinxcontrib-httpdomain/
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
..  code-block:: rst

    .. http:example:: space separated list of tools
        :request: ../optional/rel/path/to/plaintext/request
        :response: ../optional/rel/path/to/plaintext/response

        Raw plaintext HTTP request example, which is
        required only when ``:request:`` is not specified.

Example
=======
..  code-block:: rst

    .. http:example:: curl wget httpie requests

        GET /Plone/front-page HTTP/1.1
        Host: localhost:8080
        Accept: application/json
        Authorization: Basic YWRtaW46YWRtaW4=

Rendering
=========
.. http:example:: curl wget httpie requests

    GET /plone/folder/my-document?expand=breadcrumbs,navigation HTTP/1.1
    Host: localhost:8080
    Accept: application/json
    Authorization: Basic YWRtaW46c2VjcmV0


.. code:: javascript

    import PloneClient from '@plone/client';
    const cli = PloneClient.initialize({apiPath: 'http://nohost/plone'});
    const { data, status } = cli.getContent({path: '/plone/folder/my-document', expanders: ['breadcrumbs', 'navigation']})


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
