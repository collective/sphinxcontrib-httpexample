# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages

setup(
    name='sphinxcontrib-httpexample',
    version=open('VERSION').read().strip(),
    description='Adds example directive for sphinx-contrib httpdomain',
    long_description=(open('README.rst').read() + '\n' +
                      open('CHANGELOG.rst').read()),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    keywords=['sphinx', 'extension', 'http', 'rest', 'documentation'],
    author='Asko Soukka',
    author_email='asko.soukka@iki.fi',
    url='https://github.com/collective/sphinxcontrib-httpexample',
    license='GPL version 2',
    zip_safe=False,
    packages=find_packages('src'),
    namespace_packages=['sphinxcontrib'],
    package_dir={'': 'src'},
    package_data={'': ['static/*']},
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
        'pytest',
        'sphinx-testing'
    ]
)
