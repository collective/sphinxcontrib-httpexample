Examples of use:
================


Examples with inline sources
----------------------------

Example 1
^^^^^^^^^

Code
````

..  code-block:: rst

    ..  http:example:: curl wget httpie python-requests

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

.. note::

   Request and response must be separated with two or more blank lines and
   the first response line must start with string "HTTP/" or "HTTP ".

Result
``````

..  http:example:: curl wget httpie python-requests

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

or with inline response starting with just "HTTP " without the HTTP version:

..  http:example:: curl wget httpie python-requests

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


Example 2
^^^^^^^^^

Code
````

..  code-block:: rst

    ..  http:example:: curl wget httpie python-requests

        POST /Plone/folder HTTP/1.1
        Host: localhost:8080
        Accept: application/json
        Content-Type: application/json
        Authorization: Basic YWRtaW46YWRtaW4=

        {
            "@type": "Document",
            "title": "My Document"
        }

Result
``````

..  http:example:: curl wget httpie python-requests

    POST /Plone/folder HTTP/1.1
    Host: localhost:8080
    Accept: application/json
    Content-Type: application/json
    Authorization: Basic YWRtaW46YWRtaW4=

    {
        "@type": "Document",
        "title": "My Document"
    }

Example 3
^^^^^^^^^

Code
````

..  code-block:: rst

    ..  http:example:: curl wget httpie python-requests

        PATCH /Plone/folder/my-document HTTP/1.1
        Host: localhost:8080
        Content-Type: application/json
        Accept: application/json
        Authorization: Basic YWRtaW46YWRtaW4=

        {
            "title": "My New Document Title"
        }

Result
``````

..  http:example:: curl wget httpie python-requests

    PATCH /Plone/folder/my-document HTTP/1.1
    Host: localhost:8080
    Content-Type: application/json
    Accept: application/json
    Authorization: Basic YWRtaW46YWRtaW4=

    {
        "title": "My New Document Title"
    }


Example 4
^^^^^^^^^

Code
````

..  code-block:: rst

    ..  http:example:: curl wget httpie python-requests

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

    ..  http:example:: curl wget httpie python-requests

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

Example 1
^^^^^^^^^

Code
````

..  code-block:: rst

    ..  http:example:: curl wget httpie python-requests
        :request: ../tests/fixtures/001.request.txt
        :response: ../tests/fixtures/001.response.txt

Result
``````

..  http:example:: curl wget httpie python-requests
    :request: ../tests/fixtures/001.request.txt
    :response: ../tests/fixtures/001.response.txt

Example 2
^^^^^^^^^

Code
````

..  code-block:: rst

    ..  http:example:: curl wget httpie python-requests
        :request: ../tests/fixtures/002.request.txt
        :response: ../tests/fixtures/002.response.txt

Result
``````

..  http:example:: curl wget httpie python-requests
    :request: ../tests/fixtures/002.request.txt
    :response: ../tests/fixtures/002.response.txt

Example 3
^^^^^^^^^

Code
````

..  code-block:: rst

    ..  http:example:: curl wget httpie python-requests
        :request: ../tests/fixtures/003.request.txt
        :response: ../tests/fixtures/003.response.txt

Result
``````

..  http:example:: curl wget httpie python-requests
    :request: ../tests/fixtures/003.request.txt
    :response: ../tests/fixtures/003.response.txt
