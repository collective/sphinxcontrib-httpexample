Custom builder
==============



.. code:: python

   from sphinxcontrib.httpexample import register_builder
   from sphinxcontrib.httpexample import HTTPRequest

    def build_plone_client_script(request: HTTPRequest): str
        result = ""
        # ...
        return result


   register_builder(
       # Name of the builder used in the directive
       "plone-javascript",
       # Function that builds the command
       build_plone_javascript_command,
       # Language for syntax highlighting
       "javascript",
       # Display name for the documentation tab
       "@plone/client"
   )


Get content
===========

..  http:example:: curl plone-javascript

    GET /Plone/folder/my-document HTTP/1.1
    Host: localhost:8080
    Accept: application/json

..  http:example:: curl plone-javascript

    GET /Plone/folder/my-document?expand=breadcrumbs,navigation HTTP/1.1
    Host: localhost:8080
    Accept: application/json
    Authorization: Basic YWRtaW46c2VjcmV0


Update content
==============

..  http:example:: curl plone-javascript

    PATCH /Plone/folder/my-document HTTP/1.1
    Host: localhost:8080
    Content-Type: application/json
    Accept: application/json
    Authorization: Basic YWRtaW46YWRtaW4=

    {
        "title": "My New Document Title"
    }

