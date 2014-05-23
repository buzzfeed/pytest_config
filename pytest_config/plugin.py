# -*- coding: utf-8 -*-
import ConfigParser
import inspect
import os
import sys
import warnings

import pytest

from . import (
    __version__ as __pytest_version__,
    CONFIG_SECTION,
    _get_template,
    pretty
)

PROJECT_ROOT = os.getcwd()
warnings.formatwarning = pretty.formatwarning  # overwrite default warning format


###############################################################################
# Custom options to integrate with Caliendo
###############################################################################
def pytest_addoption(parser):
    caliendo_group = parser.getgroup('Caliendo', 'Caliendo specific configs')
    caliendo_group.addoption(
        '--caliendo',
        action='store_true', dest='use_caliendo', default=False,
        help='Use caliendo with your tests.')
    caliendo_group.addoption(
        '--caliendo-prefix',
        action='store', dest='caliendo_prefix', default=None,
        help='Set the destination for caliendo files.'
             'Defaults to $PWD/caliendo')
    caliendo_group.addoption(
        '--caliendo-purge',
        action='store_true',dest='purge_caliendo', default=False,
        help='Set CALIENDO_PURGE=True to clean unused caliendo files')
    caliendo_group.addoption(
        '--caliendo-prompt',
        action='store_true', dest='caliendo_prompt', default=False,
        help='Set CALIENDO_PROMPT=True to enable the caliendo prompt')

    general_group = parser.getgroup('general')
    general_group.addoption(
        '-I', '--ignore-warnings',
        action='store_true', dest='ignore_warnings', default=False,
        help='Ignore pytest_config warnings.')


###############################################################################
# This is for checking if the configuration files have bee properly updated
# to their last version, regardles if the user decided to ignore the changes
# in latest versions of this plugin
###############################################################################
def check_config_files_versions():
    def warn_outdated_version(file_name):
        with open(_get_template('outdated_conf_file.txt')) as warning:
            text = warning.read()
            pretty._print_warning(text % {'file_name': file_name})

    def error_out():
        with open(_get_template('config_section_not_found.txt')) as error:
            pretty._print_error(error.read())
        sys.exit(0)

    config = ConfigParser.ConfigParser()
    with open(os.path.join(PROJECT_ROOT, 'pytest.ini')) as current_config:
        config.readfp(current_config)
    # A pytest_config section is required in pytest.ini
    if not config.has_section(CONFIG_SECTION):
        error_out()

    # Check version of config files
    for file_name in ['pytest.ini', '.coveragerc']:
        option = file_name + '_version'
        if config.has_option(CONFIG_SECTION, option):
            if config.get(CONFIG_SECTION, option) != __pytest_version__:
                warn_outdated_version(file_name)
        else:
            error_out()

###############################################################################
# Run the appropriate setup before running the tests according to the arguments
# used.
###############################################################################
def pytest_configure(config):
    if config.getvalue('use_caliendo'):
        # Add caliendo cache variables
        os.environ.setdefault('USE_CALIENDO', 'True')

        caliendo_cache_prefix = config.getvalue('caliendo_prefix')
        if not caliendo_cache_prefix:
            caliendo_cache_prefix = os.path.join(PROJECT_ROOT, 'caliendo')
        caliendo_cache_prefix = os.path.abspath(caliendo_cache_prefix)
        os.environ.setdefault('CALIENDO_CACHE_PREFIX', caliendo_cache_prefix)

        if config.getvalue('purge_caliendo'):
            os.environ['PURGE_CALIENDO'] = 'True'

        if config.getvalue('caliendo_prompt'):
            os.environ['CALIENDO_PROMPT'] = 'True'

    if not config.getvalue('ignore_warnings'):
        check_config_files_versions()

    # Add line arguments
    config.addinivalue_line('markers', 'unit: Mark a test as a unit test. '
        'Useful for running only unit tests.')
    config.addinivalue_line('markers', 'integration: Mark a test as an '
        'integration test. Useful for running only integration tests.')


###############################################################################
# If `requests` is available, patch it so that a warning is printed when
# requests to endpoints are not properly patched.
###############################################################################
import socket
old_socket = socket.socket


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    class fake_socket(old_socket):
        def connect(self, address):
            local_stack = [s for s in inspect.stack() if os.getcwd() in s[1]]
            msg = 'YOUR TEST IS MAKING A LIVE REQUEST. LIVE REQUESTS SHOULD BE PATCHED!\n'
            for s in local_stack:
                msg += 'File "%s", line %s, in %s\n' % (s[1], s[2], s[3])
                for l in s[4]:
                    msg += l
            warnings.warn(msg, Warning)
            return super(fake_socket, self).connect(address)

    if not socket.socket == fake_socket:
        monkeypatch.setattr("socket.socket", fake_socket)


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
     - test functions/methods inside `unit/*.py` will be marked with
        `@pytest.mark.app_name` and `@pytest.mark.unit`
     - test functions/methods inside `integration/*.py` will be marked with
        `@pytest.mark.app_name` and `@pytest.mark.integration`
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
