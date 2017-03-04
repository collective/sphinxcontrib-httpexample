Basic usage
===========

Supported examples:

* curl_
* httpie_
* requests_

.. _curl: https://curl.haxx.se/
.. _httpie: https://httpie.org/
.. _requests: http://docs.python-requests.org/


With inline examples
--------------------

Code
....

..  code:: rest

    ..  http:example:: curl httpie requests

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

..  http:example:: curl httpie requests

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
----------------------

Code
....

..  code:: rest

    ..  http:example:: curl httpie requests
        :request: ../tests/fixtures/001.request.txt
        :response: ../tests/fixtures/001.response.txt

Result
......

..  http:example:: curl httpie requests
    :request: ../tests/fixtures/001.request.txt
    :response: ../tests/fixtures/001.response.txt
