# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages

setup(
    name='sphinxcontrib-httpexample',
    version=open('VERSION').read().strip(),
    description='Adds example directive for sphinx-contrib httpdomain',
    long_description=(open('README.rst').read() + '\n' +
                      open('CHANGELOG.rst').read()),
    packages=find_packages('src'),
    namespace_packages=['sphinxcontrib'],
    package_dir={'': 'src'},
    setup_requires=[
        'pytest-runner',
    ],
    install_requires=[
        'setuptools',
        'astunparse',
        'docutils',
        'sphinx',
        'sphinxcontrib-httpdomain',
    ],
    tests_require=[
        'pytest'
    ]
)
