#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pytest_config

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = pytest_config.__version__
readme = open('README.md').read()
history = open('HISTORY.md').read()

HOME = os.environ['HOME']

setup(
    name='pytest_config',
    version=version,
    description="""Base configurations and utilities for developing your Python project test suite.""",
    long_description=readme + '\n\n' + history,
    author='Gerardo Orozco Mosqueda',
    author_email='gerard.mosqueda@buzzfeed.com',
    url='https://github.com/buzzfeed/pytest_config',
    packages=['pytest_config'],
    entry_points={'pytest11': ['config = pytest_config.plugin']},
    data_files=[
        (HOME + '/.pytest_config/templates', ['data/coveragerc', 'data/pytest.ini']),
    ],
    scripts=[
        'scripts/pytest_config.init',
        'scripts/pytest_config.update'
    ],
    package_data={'pytest_config': ['_templates/*.*']},
    include_package_data=True,
    install_requires=[
        'pytest>=2.3',
        'pytest-cov==1.6',
        'pytest-cache==1.0',
        'pytest-pep8==1.0.6',
        'pytest-random==0.2'
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
