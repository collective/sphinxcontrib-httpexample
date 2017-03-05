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

Result
``````

..  http:example:: curl wget httpie python-requests

    GET /Plone/front-page HTTP/1.1
    Host: localhost:8080
    Accept: application/json
    Authorization: Basic YWRtaW46YWRtaW4=

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
