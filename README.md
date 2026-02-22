# sphinxcontrib-httpexample

<img alt="GitHub Actions" src="https://github.com/collective/sphinxcontrib-httpexample/actions/workflows/build.yml/badge.svg?branch=master" href="https://github.com/collective/sphinxcontrib-httpexample/actions">
<img alt="Coverage" src="https://coveralls.io/repos/github/collective/sphinxcontrib-httpexample/badge.svg?branch=master" href="https://coveralls.io/github/collective/sphinxcontrib-httpexample?branch=master">
<img alt="PyPI package" src="https://badge.fury.io/py/sphinxcontrib-httpexample.svg" href="https://pypi.org/project/sphinxcontrib-httpexample/">
<img alt="Documentation" src="https://readthedocs.org/projects/sphinxcontrib-httpexample/badge/?version=latest" href="https://sphinxcontrib-httpexample.readthedocs.io/en/latest/">

sphinxcontrib-httpexample is a Sphinx domain extension for describing RESTful HTTP APIs in detail.
It enhances [`sphinxcontrib-httpdomain`](https://github.com/sphinx-contrib/httpdomain) with a simple call example directive.
The directive provided by this extension generates RESTful HTTP API call examples for different HTTP clients from a single HTTP request example.

The audience for this extension are developers and technical writers documenting their RESTful HTTP APIs.
This extension was originally developed for documenting [`plone.restapi`](https://6.docs.plone.org/plone.restapi/docs/source/index.html).


## Features

-   Directive for generating various RESTful HTTP API call examples from a single HTTP request.
-   Supported HTTP clients:

    -   [curl](https://curl.haxx.se/)
    -   [wget](https://www.gnu.org/software/wget/)
    -   [httpie](https://httpie.io/)
    -   [requests](https://requests.readthedocs.io/en/stable/)

-   Custom builders, such as the [`@plone/client`](https://www.npmjs.com/package/@plone/client) package, an agnostic library that provides easy access to the Plone REST API from a client written in TypeScript.
    See https://sphinxcontrib-httpexample.readthedocs.io/en/latest/custom.html for examples.


## Examples

This extension has been used in documentation for the following projects and probably other similar projects as well.

-   https://6.docs.plone.org/plone.restapi/docs/source/index.html
-   https://sphinxcontrib-httpexample.readthedocs.io/en/latest/
-   https://guillotina.readthedocs.io/en/latest/


## Documentation

Full documentation for end users can be found in the `docs` folder.
It's also available online at https://sphinxcontrib-httpexample.readthedocs.io/en/latest/.


## Installation

Add `sphinxcontrib-httpexample` and `sphincontrib-httpdomain` to your project requirements.

Then configure your Sphinx configuration file `conf.py` with `sphinxcontrib.httpdomain` and `sphinxcontrib.httpexample` as follows.

```python
extensions = [
    "sphinxcontrib.httpdomain",
    "sphinxcontrib.httpexample",
]
```


## Contribute

To contribute to `sphinxcontrib-httpexample`, first set up your environment.


### Set up development environment

Install [uv](https://docs.astral.sh/uv/getting-started/installation/).
Carefully read the console output for further instruction.

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Initialize a Python virtual environment.

```shell
uv venv
```

Install `sphinxcontrib-httpexample`.

```shell
uv sync
```


### Build documentation

Rebuild Sphinx documentation on changes, with live reload in the browser.

```shell
make livehtml
```

To stop the preview, type `CTRL-C`.


### Run tests

```shell
make test
```


## License

The project is licensed under the GPLv2.
