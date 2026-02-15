==============
Usage examples
==============

This chapter displays reStructuredText markup examples and their renderings.

.. important::

   The request and the response must be separated by at least two blank lines, and the first line in the response must start with the string ``HTTP`` followed immediately by either a forward slash ``/`` or space character.


Examples with inline sources
----------------------------

The following examples use reStructuredText markup with the request and response sources inline with the page.


HTTP with slash and version
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following example contains an HTTP ``GET`` request.
It shows the response starting with ``HTTP`` followed by a forward slash, the HTTP version, and the HTTP response code.


Markup
``````

..  code-block:: rst

    ..  http:example:: curl wget httpie python-requests plone-client

        GET /Plone/front-page HTTP/1.1
        Host: localhost:8080
        Accept: application/json
        Authorization: Basic YWRtaW46YWRtaW4=


        HTTP/1.1 200 OK
        Content-Type: application/json

        {
          "@id": "http://localhost:8080/Plone/front-page",
          "@type": "Document",
          "UID": "1f699ffa110e45afb1ba502f75f7ec33",
          "allow_discussion": null,
          "changeNote": "",
          "contributors": [],
          "created": "2016-01-21T01:14:48+00:00",
          "creators": [
            "test_user_1_",
            "admin"
          ],
          "description": "Congratulations! You have successfully installed Plone.",
          "effective": null,
          "exclude_from_nav": false,
          "expires": null,
          "id": "front-page",
          "language": "",
          "modified": "2016-01-21T01:24:11+00:00",
          "parent": {
            "@id": "http://localhost:8080/Plone",
            "@type": "Plone Site",
            "description": "",
            "title": "Plone site"
          },
          "relatedItems": [],
          "review_state": "private",
          "rights": "",
          "subjects": [],
          "table_of_contents": null,
          "text": {
            "content-type": "text/plain",
            "data": "If you're seeing this instead of the web site you were expecting, the owner of this web site has just installed Plone. Do not contact the Plone Team or the Plone mailing lists about this.",
            "encoding": "utf-8"
          },
          "title": "Welcome to Plone"
        }

Result
``````

..  http:example:: curl wget httpie python-requests plone-client

    GET /Plone/front-page HTTP/1.1
    Host: localhost:8080
    Accept: application/json
    Authorization: Basic YWRtaW46YWRtaW4=


    HTTP/1.1 200 OK
    Content-Type: application/json

    {
      "@id": "http://localhost:8080/Plone/front-page",
      "@type": "Document",
      "UID": "1f699ffa110e45afb1ba502f75f7ec33",
      "allow_discussion": null,
      "changeNote": "",
      "contributors": [],
      "created": "2016-01-21T01:14:48+00:00",
      "creators": [
        "test_user_1_",
        "admin"
      ],
      "description": "Congratulations! You have successfully installed Plone.",
      "effective": null,
      "exclude_from_nav": false,
      "expires": null,
      "id": "front-page",
      "language": "",
      "modified": "2016-01-21T01:24:11+00:00",
      "parent": {
        "@id": "http://localhost:8080/Plone",
        "@type": "Plone Site",
        "description": "",
        "title": "Plone site"
      },
      "relatedItems": [],
      "review_state": "private",
      "rights": "",
      "subjects": [],
      "table_of_contents": null,
      "text": {
        "content-type": "text/plain",
        "data": "If you're seeing this instead of the web site you were expecting, the owner of this web site has just installed Plone. Do not contact the Plone Team or the Plone mailing lists about this.",
        "encoding": "utf-8"
      },
      "title": "Welcome to Plone"
    }

HTTP with space, no version
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following example is exactly the same as the previous one, except the response starts with ``HTTP`` without a slash and HTTP version, followed by a space and the HTTP response code.

Markup
``````

..  code-block:: rst

    ..  http:example:: curl wget httpie python-requests plone-client

        GET /Plone/front-page HTTP/1.1
        Host: localhost:8080
        Accept: application/json
        Authorization: Basic YWRtaW46YWRtaW4=


        HTTP 200 OK
        Content-Type: application/json

        {
          "@id": "http://localhost:8080/Plone/front-page",
          "@type": "Document",
          "UID": "1f699ffa110e45afb1ba502f75f7ec33",
          "allow_discussion": null,
          "changeNote": "",
          "contributors": [],
          "created": "2016-01-21T01:14:48+00:00",
          "creators": [
            "test_user_1_",
            "admin"
          ],
          "description": "Congratulations! You have successfully installed Plone.",
          "effective": null,
          "exclude_from_nav": false,
          "expires": null,
          "id": "front-page",
          "language": "",
          "modified": "2016-01-21T01:24:11+00:00",
          "parent": {
            "@id": "http://localhost:8080/Plone",
            "@type": "Plone Site",
            "description": "",
            "title": "Plone site"
          },
          "relatedItems": [],
          "review_state": "private",
          "rights": "",
          "subjects": [],
          "table_of_contents": null,
          "text": {
            "content-type": "text/plain",
            "data": "If you're seeing this instead of the web site you were expecting, the owner of this web site has just installed Plone. Do not contact the Plone Team or the Plone mailing lists about this.",
            "encoding": "utf-8"
          },
          "title": "Welcome to Plone"
        }


Result
``````

..  http:example:: curl wget httpie python-requests plone-client

    GET /Plone/front-page HTTP/1.1
    Host: localhost:8080
    Accept: application/json
    Authorization: Basic YWRtaW46YWRtaW4=


    HTTP 200 OK
    Content-Type: application/json

    {
      "@id": "http://localhost:8080/Plone/front-page",
      "@type": "Document",
      "UID": "1f699ffa110e45afb1ba502f75f7ec33",
      "allow_discussion": null,
      "changeNote": "",
      "contributors": [],
      "created": "2016-01-21T01:14:48+00:00",
      "creators": [
        "test_user_1_",
        "admin"
      ],
      "description": "Congratulations! You have successfully installed Plone.",
      "effective": null,
      "exclude_from_nav": false,
      "expires": null,
      "id": "front-page",
      "language": "",
      "modified": "2016-01-21T01:24:11+00:00",
      "parent": {
        "@id": "http://localhost:8080/Plone",
        "@type": "Plone Site",
        "description": "",
        "title": "Plone site"
      },
      "relatedItems": [],
      "review_state": "private",
      "rights": "",
      "subjects": [],
      "table_of_contents": null,
      "text": {
        "content-type": "text/plain",
        "data": "If you're seeing this instead of the web site you were expecting, the owner of this web site has just installed Plone. Do not contact the Plone Team or the Plone mailing lists about this.",
        "encoding": "utf-8"
      },
      "title": "Welcome to Plone"
    }


HTTP ``POST``
^^^^^^^^^^^^^

The following example contains an HTTP ``POST`` request and its response.


Markup
``````

..  code-block:: rst

    ..  http:example:: curl wget httpie python-requests plone-client

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

Result
``````

..  http:example:: curl wget httpie python-requests plone-client

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


HTTP ``PATCH``
^^^^^^^^^^^^^^

The following example contains an HTTP ``PATCH`` request and its response.


Markup
``````

..  code-block:: rst

    ..  http:example:: curl wget httpie python-requests plone-client

        PATCH /Plone/folder/my-document HTTP/1.1
        Host: localhost:8080
        Content-Type: application/json
        Accept: application/json
        Authorization: Basic YWRtaW46YWRtaW4=


        HTTP 200 OK
        Content-Type: application/json

        {
            "title": "My New Document Title"
        }

Result
``````

..  http:example:: curl wget httpie python-requests plone-client

    PATCH /Plone/folder/my-document HTTP/1.1
    Host: localhost:8080
    Content-Type: application/json
    Accept: application/json
    Authorization: Basic YWRtaW46YWRtaW4=


    HTTP 200 OK
    Content-Type: application/json

    {
        "title": "My New Document Title"
    }


Query parameters
^^^^^^^^^^^^^^^^

This example appends query parameters to the request's query string.
The response is omitted.

Markup
``````

..  code-block:: rst

    ..  http:example:: curl wget httpie python-requests plone-client

        GET /items?user_id=12&user_id=13 HTTP/1.1
        Host: localhost
        Accept: application/json
        Authorization: Basic YWRtaW46YWRtaW4=

        :query from: 20170101
        :query to: 20171231
        :query user_id: 15
        :query limit: 20
        :query sort: date-asc


Result
``````

    ..  http:example:: curl wget httpie python-requests plone-client

        GET /items?user_id=12&user_id=13 HTTP/1.1
        Host: localhost
        Accept: application/json
        Authorization: Basic YWRtaW46YWRtaW4=

        :query from: 20170101
        :query to: 20171231
        :query user_id: 15
        :query limit: 20
        :query sort: date-asc


Examples with external sources
------------------------------

The following examples demonstrate the use of external source files.
These files can also be used in tests to ensure their validity.

HTTP ``GET``
^^^^^^^^^^^^

Markup
``````

..  code-block:: rst

    ..  http:example:: curl wget httpie python-requests plone-client
        :request: ../tests/fixtures/001.request.txt
        :response: ../tests/fixtures/001.response.txt

Result
``````

..  http:example:: curl wget httpie python-requests plone-client
    :request: ../tests/fixtures/001.request.txt
    :response: ../tests/fixtures/001.response.txt

HTTP ``POST``
^^^^^^^^^^^^^

Markup
``````

..  code-block:: rst

    ..  http:example:: curl wget httpie python-requests plone-client
        :request: ../tests/fixtures/002.request.txt
        :response: ../tests/fixtures/002.response.txt

Result
``````

..  http:example:: curl wget httpie python-requests plone-client
    :request: ../tests/fixtures/002.request.txt
    :response: ../tests/fixtures/002.response.txt


HTTP ``PATCH``
^^^^^^^^^^^^^^


Markup
``````

..  code-block:: rst

    ..  http:example:: curl wget httpie python-requests plone-client
        :request: ../tests/fixtures/003.request.txt
        :response: ../tests/fixtures/003.response.txt

Result
``````

..  http:example:: curl wget httpie python-requests plone-client
    :request: ../tests/fixtures/003.request.txt
    :response: ../tests/fixtures/003.response.txt


Examples with tab libraries
---------------------------

`sphinx-inline-tabs <https://sphinx-inline-tabs.readthedocs.io/en/latest/>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Markup
``````

..  code-block:: rst

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

    ..  tab:: python-requests

        ..  http:example-block:: wget
            :request: ../tests/fixtures/001.request.txt

    ..  tab:: plone-client

        ..  http:example-block:: wget
            :request: ../tests/fixtures/001.request.txt

    ..  tab:: response

        ..  http:example-block:: response
            :response: ../tests/fixtures/001.response.txt

Result
``````

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

..  tab:: python-requests

  ..  http:example-block:: wget
      :request: ../tests/fixtures/001.request.txt

..  tab:: plone-client

  ..  http:example-block:: wget
      :request: ../tests/fixtures/001.request.txt

..  tab:: response

  ..  http:example-block:: response
      :response: ../tests/fixtures/001.response.txt


`sphinx-design <https://sphinx-design.readthedocs.io/en/furo-theme/tabs.html>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Markup
``````

..  code-block:: rst

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

      ..  tab-item:: python-requests

          ..  http:example-block:: wget
              :request: ../tests/fixtures/001.request.txt

      ..  tab-item:: plone-client

          ..  http:example-block:: wget
              :request: ../tests/fixtures/001.request.txt

      ..  tab-item:: response

          ..  http:example-block:: response
              :response: ../tests/fixtures/001.response.txt

Result
``````

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

  ..  tab-item:: python-requests

      ..  http:example-block:: wget
          :request: ../tests/fixtures/001.request.txt

  ..  tab-item:: plone-client

      ..  http:example-block:: wget
          :request: ../tests/fixtures/001.request.txt

  ..  tab-item:: response

      ..  http:example-block:: response
          :response: ../tests/fixtures/001.response.txt
