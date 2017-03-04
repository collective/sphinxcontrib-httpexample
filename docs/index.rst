.. sphinxcontrib-httpexample documentation master file, created by
   sphinx-quickstart on Fri Mar  3 12:29:43 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to sphinxcontrib-httpexample's documentation!
=====================================================

Contents:

..  toctree::
    :maxdepth: 2


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

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

