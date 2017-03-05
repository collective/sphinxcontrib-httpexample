===========
Basic usage
===========

Supported examples:

* curl_
* httpie_
* python-requests_

.. _curl: https://curl.haxx.se/
.. _httpie: https://httpie.org/
.. _python-requests: http://docs.python-requests.org/


With inline examples
====================

Example 1
---------

Code
....

..  code:: rest

    ..  http:example:: curl httpie python-requests

        GET /Plone/front-page HTTP/1.1
        Host: localhost:8080
        Accept: application/json
        Authorization: Basic YWRtaW46YWRtaW4=

Result
......

..  http:example:: curl httpie python-requests

    GET /Plone/front-page HTTP/1.1
    Host: localhost:8080
    Accept: application/json
    Authorization: Basic YWRtaW46YWRtaW4=

Example 2
---------

Code
....

..  code:: rest

    ..  http:example:: curl httpie python-requests

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
......

..  http:example:: curl httpie python-requests

    POST /Plone/folder HTTP/1.1
    Host: localhost:8080
    Accept: application/json
    Content-Type: application/json
    Authorization: Basic YWRtaW46YWRtaW4=

    {
        "@type": "Document",
        "title": "My Document"
    }


With included examples
======================

Example 1
---------

Code
....

..  code:: rest

    ..  http:example:: curl httpie python-requests
        :request: ../tests/fixtures/001.request.txt
        :response: ../tests/fixtures/001.response.txt

Result
......

..  http:example:: curl httpie python-requests
    :request: ../tests/fixtures/001.request.txt
    :response: ../tests/fixtures/001.response.txt

Example 2
---------

Code
....

..  code:: rest

    ..  http:example:: curl httpie python-requests
        :request: ../tests/fixtures/002.request.txt
        :response: ../tests/fixtures/002.response.txt

Result
......

..  http:example:: curl httpie python-requests
    :request: ../tests/fixtures/002.request.txt
    :response: ../tests/fixtures/002.response.txt
