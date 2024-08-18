Changelog
=========

1.3 (unreleased)
----------------

- Add new directive `.. http:example-block::` to allow use with Sphinx tab libraries like
  `sphinx-inline-tabs <https://sphinx-inline-tabs.readthedocs.io/en/latest/>`_ or
  `sphinx-design <https://sphinx-design.readthedocs.io/en/furo-theme/tabs.html>`_.
  [AWhetter]

1.2 (2024-08-17)
----------------

- Add new HTTP example builder `plone-javascript`
  [datakurre]

- Fix tabbing to no longer depend on jQuery
  [datakurre]

- Fix tabbing to support arrow key navigation
  [datakurre]

- Fix tab key to stop at tab list only once
  [datakurre]

- Fix requests builder to flatten simple values in form data
  [datakurre]

- Fix requests builder to pass form data as dictionary
  [datakurre]

- Change JavaScript-based tabbing to no longer require JQuery
  [datakurre]

1.1 (2021-12-25)
----------------

- Add support for docutils 0.17.x
  [kvondersaar, datakurre]
- Add support for Python 3.8
  [datakurre]
- Fix example tabs accessibility
  [datakurre]

1.0 (2021-09-10)
----------------

- The curl command builder will now always specify a method
  [LefterisJP]

0.11.0 (2021-05-14)
-------------------

- Change to quote examples with " rather than '
  [datakurre]
- Fix Sphinx deprecation warnings and support Sphinx 4.x]
  [kkrypt0nn,  AWhetter]
- Fix to use ast.unparse instead astunparse on Python >= 3.9
  [datakurre]

0.10.3 (2019-05-01)
-------------------

- Re-release 0.10.2 with wheel
  [datakurre]


0.10.2 (2019-05-01)
-------------------

- Add support for inline response examples without HTTP version
  (e.g. `HTTP 200 OK`)
  [datakurre]

- Fix regression where support for reading request examples from
  external files was broken since 0.10.0
  [datakurre]

0.10.1 (2019-03-19)
-------------------

- Fix issue where it was not possible to request exmples with
  float values in payload JSON [fixes #42]
  [datakurre]

0.10.0 (2018-10-09)
-------------------

- Add support of the URL query parameters, using the `query` field.
  Given a line `:query param_name: param_value` in an http example
  directive, the key value pair `param_name`, `param_value` will be
  added to the request URL (and excluded from further processing).
  [ludaavics]

  Example::

      GET /items HTTP/1.1
      Host: localhost
      Accept: application/json
      Authorization: Basic dXNlcjpwYXNzd29yZA==

      :query from: 20170101
      :query to: 20171231
      :query user_id: 12
      :query limit: 20
      :query sort: date(asc)

0.9.1 (2018-10-06)
------------------

- Fix packaging to include setup.cfg in sdist
  [datakurre]
- Add the guillotina docs (which now uses httpexample)
  [cdevienne]

0.9.0 (2018-07-22)
------------------

- Add support for inlining responses
  [cdevienne]

0.8.1 (2018-06-27)
------------------

- Fixed error when parsing top level json lists
  [AWhetter]

0.8.0 (2017-11-18)
------------------

- Fix to not strip out Accept/Content-Type headers in builders
  [dokai]

- Improve logic to detect a JSON content type
  [dokai]

- Use redirected input to pass request payload to httpie
  [dokai]

- Fix quoting of non-trivial HTTP headers in builders
  [dokai]

- Change to use declarative packaging (setup.cfg instead of setup.py)
  [datakurre]


0.7.0 (2017-10-21)
------------------

- Allow the URL scheme (http or https) to be configured
  [dokai]

- Quote the URL if it contains `&` characters in curl/httpie/wget examples
  [dokai]


0.6.1 (2017-05-11)
------------------

- Release as universal wheel
  [datakurre]


0.6.0 (2017-05-11)
------------------

- Support non-json requests
  [jaroel]

- Support application/json; charset=utf-8
  [skyzyx]


0.5.2 (2017-03-09)
------------------

- Fix packaging to include the files in static #3
  [csenger]


0.5.1 (2017-03-05)
------------------

- Update README and documentation
  [datakurre]


0.5.0 (2017-03-05)
------------------

- Change development status to beta
  [datakurre]


0.4.2 (2017-03-05)
------------------

- Fix issue where wget basic auth required challenge from backend, which is not
  always available
  [datakurre]


0.4.1 (2017-03-05)
------------------

- Fix issue where generate httpie-commands did not always set Accept and
  Content-Type -headers
  [datakurre]


0.4.0 (2017-03-05)
------------------

- Add support for wget
  [datakurre]


0.3.0 (2017-03-05)
------------------

- Add generic 'Authorization'-header support
  [datakurre]


0.2.1 (2017-03-05)
------------------

- Fix issue where Authorization-header was always requires
  [datakurre]
- Fix raise proper exception when parsing bad requests
  [datakurre]
- Fix issue where httpie-builder did not quote values with spaces
  [datakurre]
- Fix link to python-requests' documentation
  [datakurre]


0.2.0 (2017-03-05)
------------------

- Add support for GET requests
  [datakurre]


0.1.0 (2017-03-05)
------------------

- First release
  [datakurre]
