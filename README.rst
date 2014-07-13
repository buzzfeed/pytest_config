pytest-config
===============

.. image:: https://pypip.in/v/pytest-config/badge.svg
    :target: https://crate.io/packages/pytest-config/
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/pytest-config/badge.png
    :target: https://crate.io/packages/pytest-config/
    :alt: Number of PyPI downloads

.. image:: https://pypip.in/format/pytest-config/badge.png
    :target: https://pypi.python.org/pypi/pytest-config/
    :alt: Download format

Base configurations and utilities for developing your Python project test suite.

Installation
============

.. code-block::

    pip install git+git://github.com/buzzfeed/pytest_config.git@<version>#egg=pytest_config==<version>

This will install:

- pytest_config ``py.test`` plugin
- a simple django app that extends the ``django-admin.py startapp`` (under development).
- a ``pytest_config.init`` command to initialize new config files
- a ``pytest_config.update`` command to interactively update your config files
  against the lates default values.

Features
========

Automatic fix for the sys.path known issue.
-------------------------------------------

``pytest_config`` takes care of the ``sys.path`` known issue_ between pytest and pytest-django
by automatically adding the current working directory to the ``PYTHONPATH`` before tests run.

.. _issue: http://pytest-django.readthedocs.org/en/latest/faq.html#i-see-an-error-saying-could-not-import-myproject-settings

Management of configuration files
---------------------------------

.. code-block::

    $ pytest_config.init [options]

This command will copy all the configuration files needed to easily configure
``py.test`` and ``coverage``. Beware of this command as **it will simply replace any
existing config files in you current directory**.

.. code-block::

    $ pytest_config.update [options]

This command will read the default configuration files and your customized
configuration files. If any of the options in you custom configuration differs
from the defaults, you will be prompted if you want to keep the current one.
If you decline, the default will be saved to your local configuration.

Available options
-----------------

The two previous commands share a few of their interface, which is as follows:

- ``pytest_config.[init|update] -h`` prints the help page.
- ``pytest_config.[init|update] --coverage`` makes the command apply its operations
  only for the ``.coveragerc`` file.
- ``pytest_config.[init|update] --pytest-ini`` makes the command apply its operations
- only for the ``pytest.ini`` file.

``pytest_config.update`` has additional options, though:

- ``pytest_config.update -y`` silences the process so that you are not prompted
  about anything. All the defaults will be automatically applied if you use this.

Automatic test marking
----------------------

``pytest_config`` automatically marks your tests at runtime with markers based on
what directories the tests are in, so under this architecture:

.. code-block::

    project_root/
        app_name/
        tests/  # root `tests` directory
            ├── __init__.py
            └── app_name/
                ├── __init__.py
                ├── integration/
                │   ├── __init__.py
                │   └── test_foo.py
                └── unit/
                    ├── __init__.py
                    └── test_bar.py

- test functions/methods inside ``app_name/unit/*.py`` will be marked with
  ``@pytest.mark.<app_name>`` and ``@pytest.mark.unit``
- test functions/methods inside ``app_name/integration/*.py`` will be marked with
  ``@pytest.mark.<app_name>`` and ``@pytest.mark.integration``

and so on. This will allow you to run tests on a per-app and per-type basis by running:

.. code-block::

    $ py.test -m unit
    $ py.test -m integration
    $ py.test -m app_name
    $ py.test -m 'app_name and <type>'
    $ py.test -m '<type> and app_name'

Integration with Caliendo
-------------------------

The following command line arguments have been added to `py.test` to integrate it
smoothly with Caliendo_:

.. _Caliendo: https://github.com/buzzfeed/caliendo

- ``py.test --caliendo``: Enable the overall use of `caliendo` in your tests.
- ``py.test --caliendo-prefix path/to/caliendo/files``: Set the path to where the caliendo
  files should live. If you are defining this yourself, it's recommended that you set it as a path
  relative to your current working directory, i.e. ``caliendo``, ``./caliendo``,
  ``whatever/caliendo`` and not as an absolute path. Defaults to ``$PWD/caliendo``.
- ``py.test --caliendo --caliendo-purge``: Set the ``CALIENDO_PURGE`` environment variable so that
  caliendo can get rid of unused cache, evs, etc.
- ``py.test --caliendo --caliendo-prompt``: Set the ``CALIENDO_PROMPT`` environment variable
  so that you may use the interactive prompt_ built in caliendo

.. _prompt: https://github.com/buzzfeed/caliendo#configuration
