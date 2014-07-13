#!/usr/bin/env python
import os
import pytest_config

from setuptools import setup


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


HOME = os.environ['HOME']

setup(
    name='pytest-config',
    version=pytest_config.__version__,
    description="""
    Base configurations and utilities for developing
    your Python project test suite with pytest.
    """,
    long_description=read('README.rst'),
    author='Gerardo Orozco Mosqueda',
    author_email='gerard.mosqueda@buzzfeed.com',
    url='https://github.com/buzzfeed/pytest_config',
    packages=['pytest_config'],
    entry_points={'pytest11': ['config = pytest_config.plugin']},
    data_files=[
        (os.path.join(HOME, '.pytest_config/templates'),
         ['data/coveragerc', 'data/pytest.ini']),
    ],
    scripts=[
        'scripts/pytest_config.init',
        'scripts/pytest_config.update'
    ],
    package_data={'pytest_config': ['_templates/*.*']},
    include_package_data=True,
    install_requires=[
        'pytest>=2.3',
        'pytest-django>=2.6.1',
        'pytest-cov>=1.6',
        'pytest-cache>=1.0',
        'pep8>=1.5.6',
        'pytest-pep8>=1.0.6',
        'pytest-random>=0.2',
        'pytest-pythonpath==0.3'
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
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
