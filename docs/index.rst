Sphinx directive for RESTful HTTP API examples
==============================================

sphinxcontrib-httpexample enhances `sphinxcontrib-httpdomain`_, a Sphinx domain extension for describing RESTful HTTP APIs in detail, with a simple call example directive. The new directive provided by this extension generates RESTful HTTP API call examples for different tools from a single HTTP request example.

The audience for this extension are developers and technical writes documenting their RESTful HTTP APIs. This extension has originally been developed for documenting `plone.restapi`_.

.. _sphinxcontrib-httpdomain: https://pythonhosted.org/sphinxcontrib-httpdomain/
.. _plone.restapi: http://plonerestapi.readthedocs.org/

* Configuration:

  The URL scheme, either ``http`` or ``https``, used in the generated examples
  can be configured with the ``httpexample_scheme`` configuration variable. It
  defaults to ``http``.

  ..  code-block:: python

      # conf.py
      httpexample_scheme = 'https'

* Syntax:

  ..  code-block:: rst

      .. http:example:: space separated list of tools
         :request: ../optional/rel/path/to/plaintext/request
         :response: ../optional/rel/path/to/plaintext/response

         Raw plaintext HTTP request example, which is
         required only when :request: is not specified.

* Example:

  ..  code-block:: rst

      ..  http:example:: curl wget httpie python-requests

          GET /Plone/front-page HTTP/1.1
          Host: localhost:8080
          Accept: application/json
          Authorization: Basic YWRtaW46YWRtaW4=

* Rendering:

  ..  http:example:: curl wget httpie python-requests

      GET /Plone/front-page HTTP/1.1
      Host: localhost:8080
      Accept: application/json
      Authorization: Basic YWRtaW46YWRtaW4=

* Supported tools:

  - curl_
  - wget_
  - httpie_
  - python-requests_

.. _curl: https://curl.haxx.se/
.. _wget: https://www.gnu.org/software/wget/
.. _httpie: https://httpie.org/
.. _python-requests: http://docs.python-requests.org/

..  toctree::
    :maxdepth: 2

    usage
