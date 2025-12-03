sphinxcontrib-httpexample
=========================

.. image:: https://github.com/collective/sphinxcontrib-httpexample/actions/workflows/build.yml/badge.svg?branch=master
   :target: https://github.com/collective/sphinxcontrib-httpexample/actions

.. image:: https://coveralls.io/repos/github/collective/sphinxcontrib-httpexample/badge.svg?branch=master
   :target: https://coveralls.io/github/collective/sphinxcontrib-httpexample?branch=master

.. image:: https://badge.fury.io/py/sphinxcontrib-httpexample.svg
   :target: https://badge.fury.io/py/sphinxcontrib-httpexample

.. image:: https://readthedocs.org/projects/sphinxcontrib-httpexample/badge/?version=latest
   :target: http://sphinxcontrib-httpexample.readthedocs.io/en/latest

sphinxcontrib-httpexample enhances `sphinxcontrib-httpdomain`_, a Sphinx domain extension for describing RESTful HTTP APIs in detail, with a simple call example directive. The new directive provided by this extension generates RESTful HTTP API call examples for different tools from a single HTTP request example.

The audience for this extension are developers and technical writes documenting their RESTful HTTP APIs. This extension has originally been developed for documenting `plone.restapi`_.

.. _sphinxcontrib-httpdomain: https://pythonhosted.org/sphinxcontrib-httpdomain/
.. _plone.restapi: http://plonerestapi.readthedocs.org/


Features
--------

* Directive for generating various RESTful HTTP API call examples from single HTTP request.

* Supported tools:

  - curl_
  - wget_
  - httpie_
  - python-requests_

.. _curl: https://curl.haxx.se/
.. _wget: https://www.gnu.org/software/wget/
.. _httpie: https://httpie.org/
.. _python-requests: http://docs.python-requests.org/


Examples
--------

This extension has been used at least in the following documentations:

* http://plonerestapi.readthedocs.org/
* http://sphinxcontrib-httpexample.readthedocs.org/
* https://guillotina.readthedocs.io/en/latest/


Documentation
-------------

Full documentation for end users can be found in the "docs" folder. It is also available online at http://sphinxcontrib-httpexample.readthedocs.org/


Installation
------------

Add sphinxcontrib-httpexample into requirements of your product documentation and into the configuration file of your Sphinx documentation next to sphincontrib-httpdomain as follows:

..  code:: python

    extensions = ['sphinxcontrib.httpdomain', 'sphinxcontrib.httpexample']


## Contribute

```shell
uv venv
uv sync
make watch
```

Yields

```console
$ make watch
PYTHONPATH=/Users/stevepiercy/projects/sphinxcontrib-httpexample/docs sphinx-autobuild -b html docs docs/html
[sphinx-autobuild] > sphinx-build -b html /Users/stevepiercy/projects/sphinxcontrib-httpexample/docs /Users/stevepiercy/projects/sphinxcontrib-httpexample/docs/html
Running Sphinx v4.5.0

Configuration error:
There is a programmable error in your configuration file:

Traceback (most recent call last):
  File "/Users/stevepiercy/.pyenv/versions/3.10.13/lib/python3.10/site-packages/sphinx/config.py", line 332, in eval_config_file
    exec(code, namespace)
  File "/Users/stevepiercy/projects/sphinxcontrib-httpexample/docs/conf.py", line 86, in <module>
    dist = metadata.distribution("sphinxcontrib-httpexample")
  File "/Users/stevepiercy/.pyenv/versions/3.10.13/lib/python3.10/importlib/metadata/__init__.py", line 969, in distribution
    return Distribution.from_name(distribution_name)
  File "/Users/stevepiercy/.pyenv/versions/3.10.13/lib/python3.10/importlib/metadata/__init__.py", line 548, in from_name
    raise PackageNotFoundError(name)
importlib.metadata.PackageNotFoundError: No package metadata was found for sphinxcontrib-httpexample

Command exited with exit code: 2
The server will continue serving the build folder, but the contents being served are no longer in sync with the documentation sources. Please fix the cause of the error above or press Ctrl+C to stop the server.
[I 251202 22:42:04 server:335] Serving on http://127.0.0.1:8000
[I 251202 22:42:04 handlers:62] Start watching changes
```


License
-------

The project is licensed under the GPLv2.
