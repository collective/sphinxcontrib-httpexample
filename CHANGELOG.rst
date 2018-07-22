Changelog
=========

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
