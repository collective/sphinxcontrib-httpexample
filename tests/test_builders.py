# -*- coding: utf-8 -*-
from .test_fixtures import FIXTURE_001_REQUEST
from .test_fixtures import FIXTURE_002_REQUEST
from .test_fixtures import FIXTURE_003_REQUEST
from .test_fixtures import FIXTURE_004_REQUEST
from .test_fixtures import FIXTURE_005_REQUEST
from .test_fixtures import FIXTURE_006_REQUEST
from .test_fixtures import FIXTURE_007_REQUEST
from .test_fixtures import FIXTURE_008_REQUEST
from .test_fixtures import FIXTURE_009_REQUEST
from .test_fixtures import FIXTURE_011_REQUEST
from .test_fixtures import FIXTURE_012_REQUEST
from sphinxcontrib.httpexample.builders import build_curl_command
from sphinxcontrib.httpexample.builders import build_httpie_command
from sphinxcontrib.httpexample.builders import build_requests_command
from sphinxcontrib.httpexample.builders import build_wget_command
from sphinxcontrib.httpexample.parsers import parse_request

import pytest


request_fixtures = (
    {'name': 'fixture_001', 'data': FIXTURE_001_REQUEST},
    {'name': 'fixture_002', 'data': FIXTURE_002_REQUEST},
    {'name': 'fixture_003', 'data': FIXTURE_003_REQUEST},
    {'name': 'fixture_004', 'data': FIXTURE_004_REQUEST},
    {'name': 'fixture_005', 'data': FIXTURE_005_REQUEST},
    {'name': 'fixture_006', 'data': FIXTURE_006_REQUEST},
    {'name': 'fixture_007', 'data': FIXTURE_007_REQUEST},
    {'name': 'fixture_008', 'data': FIXTURE_008_REQUEST},
    {'name': 'fixture_009', 'data': FIXTURE_009_REQUEST},
    {'name': 'fixture_011', 'data': FIXTURE_011_REQUEST},
    {'name': 'fixture_012', 'data': FIXTURE_012_REQUEST},
)


@pytest.mark.parametrize(
    'request_fixture',
    request_fixtures,
    ids=[fixture['name'] for fixture in request_fixtures],
)
@pytest.mark.parametrize('builder', (
    build_httpie_command,
    build_curl_command,
    build_wget_command,
    build_requests_command,
), ids=lambda fn: fn.__name__)
def test_fixture(request_fixture, builder, snapshot):
    command = builder(parse_request(request_fixture['data']))
    snapshot.assert_match(command)
