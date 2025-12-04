# sphinxcontrib-httpexample

<img alt="GitHub Actions" src="https://github.com/collective/sphinxcontrib-httpexample/actions/workflows/build.yml/badge.svg?branch=master" href="https://github.com/collective/sphinxcontrib-httpexample/actions">
<img alt="Coverage" src="https://coveralls.io/repos/github/collective/sphinxcontrib-httpexample/badge.svg?branch=master" href="https://coveralls.io/github/collective/sphinxcontrib-httpexample?branch=master">
<img alt="PyPI package" src="https://badge.fury.io/py/sphinxcontrib-httpexample.svg" href="https://badge.fury.io/py/sphinxcontrib-httpexample">
<img alt="Documentation" src="https://readthedocs.org/projects/sphinxcontrib-httpexample/badge/?version=latest" href="http://sphinxcontrib-httpexample.readthedocs.io/en/latest">

sphinxcontrib-httpexample enhances [`sphinxcontrib-httpdomain`](https://pythonhosted.org/sphinxcontrib-httpdomain/), a Sphinx domain extension for describing RESTful HTTP APIs in detail, with a simple call example directive. The new directive provided by this extension generates RESTful HTTP API call examples for different tools from a single HTTP request example.

The audience for this extension are developers and technical writes documenting their RESTful HTTP APIs. This extension has originally been developed for documenting [`plone.restapi`](https://6.docs.plone.org/plone.restapi/docs/source/index.html).


## Features

-   Directive for generating various RESTful HTTP API call examples from single HTTP request.
-   Supported tools:

    -   [curl](https://curl.haxx.se/)
    -   [wget](https://www.gnu.org/software/wget/)
    -   [httpie](https://httpie.org/)
    -   [python-requests](http://docs.python-requests.org/)


## Examples

This extension has been used at least in the following documentations:

-   https://6.docs.plone.org/plone.restapi/docs/source/index.html
-   https://sphinxcontrib-httpexample.readthedocs.org/en/latest/
-   https://guillotina.readthedocs.io/en/latest/


## Documentation

Full documentation for end users can be found in the "docs" folder. It is also available online at http://sphinxcontrib-httpexample.readthedocs.org/


## Installation

Add `sphinxcontrib-httpexample` and `sphincontrib-httpdomain` into your project requirements.

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

Install [uv](https://6.docs.plone.org/glossary.html#term-uv).
Carefully read the console output for further instructions, and follow them, if needed.

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

Rebuild Sphinx documentation on changes, with live-reload in the browser

```shell
make livehtml
```

To stop the preview, type `CTRL-C`.


### Run tests

make te

## License

The project is licensed under the GPLv2.
