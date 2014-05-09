# -*- coding: utf-8 -*-
import os
import pytest

PROJECT_ROOT = os.environ.get('PWD')


def pytest_addoption(parser):
    group = parser.getgroup('BuzzFeed', 'BuzzFeed specific configs')
    group.addoption('--caliendo',
                    action='store_true', dest='use_caliendo', default=False,
                    help='Use caliendo with your tests.')
    group.addoption('--caliendo-prefix',
                    action='store', dest='caliendo_prefix', default=None,
                    help='Set the destination for caliendo files. Defaults to $PWD/caliendo')
    group.addoption('--caliendo-purge',
                    action='store_true',dest='purge_caliendo', default=False,
                    help='Set CALIENDO_PURGE=True to clean unused caliendo files')


def pytest_configure(config):
    if config.getvalue('use_caliendo'):
        # Add caliendo cache variables
        os.environ.setdefault('USE_CALIENDO', 'True')
        CALIENDO_CACHE_PREFIX = config.getvalue('caliendo_prefix')
        if not CALIENDO_CACHE_PREFIX:
            CALIENDO_CACHE_PREFIX = os.path.join(PROJECT_ROOT, 'caliendo')
        os.environ.setdefault('CALIENDO_CACHE_PREFIX', CALIENDO_CACHE_PREFIX)

    # Add line arguments
    config.addinivalue_line('markers', 'unit: Mark a test as a unit test. Useful for running only unit tests.')
    config.addinivalue_line('markers', 'integration: Mark a test as an integration test. Useful for running only integration tests.')


def pytest_collection_modifyitems(items):
    apply_test_type_markers(items)


def apply_test_type_markers(items):
    """
    Apply markers to tests based on what tests directory they are under.
    This assumes the root `tests` directory is organized in a per-app basis
    as follows:

        tests/  # root `tests` directory
        ├── __init__.py
        └── app_name
            ├── __init__.py
            ├── integration
            │   ├── __init__.py
            │   └── test_foo.py
            └── unit
                ├── __init__.py
                └── test_bar.py

    Under this architecture:
     - test functions/methods inside `unit/*.py` will be marked with `@pytest.mark.app_name` and `@pytest.mark.unit`
     - test functions/methods inside `integration/*.py` will be marked with `@pytest.mark.app_name` and `@pytest.mark.integration`
    and so on, based on what types of tests you need to write and run.

    This will allow you to run tests on a per-app and per-type basis by running:

        $ py.test -m unit
        $ py.test -m integration
        $ py.test -m app_name
        $ py.test -m 'app_name and <type>'
        $ py.test -m '<type> and app_name'

    """
    import _pytest
    for item in items:
        if isinstance(item, _pytest.python.Function):
            module_name = item.module.__name__
            root, app_name, test_type, test_descriptor = module_name.split('.', 3)
            # mark tests by app name
            item.add_marker(getattr(pytest.mark, app_name))
            # mark tests by tetsing type
            item.add_marker(getattr(pytest.mark, test_type))
