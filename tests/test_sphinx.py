# -*- coding: utf-8 -*-
import pytest


@pytest.yield_fixture(scope='module')
def rest_mock(request):
    return None


def test_dummy(rest_mock):
    assert True


# a) Override CodeBlock-direcitive
# b) Register explicit REST example directive to sphinx
# c) Register magical coodeblock lexer

# - test exampe generator

# On directive read, generate required examples
# - test docutils integratoin
