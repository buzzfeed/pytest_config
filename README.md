# pytest-config

Base configurations and utilities for developing your Python project test suite.

### Installation

    pip install git+git://github.com/buzzfeed/pytest_config.git@0.0.1#egg=pytest_config==0.0.1

**NOTE**: Please install `pytest_config` from you project root,
as it depends on the current directory to copy some files.

This will install the `py.test` plugin and make available a simple django app
that extends the `django-admin.py startapp` (under development).
Also, `pytest.ini` and `.coveragerc` files will be copied to your current
directory. These files are templates that you can modify as needed.

### Features

#### Automatic test marking

pytest_config automatically marks your tests at runtime with markers based on
what directories the tests are in, so under this architecture:

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

- test functions/methods inside `app_name/unit/*.py` will be marked with
`@pytest.mark.<app_name>` and `@pytest.mark.unit`
- test functions/methods inside `app_name/integration/*.py` will be marked with
`@pytest.mark.<app_name>` and `@pytest.mark.integration`

and so on. This will allow you to run tests on a per-app and per-type basis by running:

    $ py.test -m unit
    $ py.test -m integration
    $ py.test -m app_name
    $ py.test -m 'app_name and <type>'
    $ py.test -m '<type> and app_name'

#### Integration with Caliendo

The following command line arguments have been added to `py.test` to integrate it
smoothly with [caliendo](https://github.com/buzzfeed/caliendo).

###### --caliendo

Running `py.test` with `--caliendo` will enable the overall use of `caliendo`
in your tests

    $ py.test --caliendo

###### --caliendo-prefix *

The `--caliendo-prefix` option will set the path to where the caliendo files
should live. If you are defining this yourself, it's recommended that you set
it as a path relative to your current working directory, i.e. `caliendo`, `./caliendo`, `whatever/caliendo`

    $ py.test --caliendo --caliendo-prefix [path_to_caliendo_files]

###### --caliendo-purge *

The `--caliendo-purge` option will set the CALIENDO_PURGE environment variable
so that caliendo can get rid of unused cache/evs/etc.

    $ py.test --caliendo --caliendo-purge

###### --caliendo-prompt *

The `--caliendo-prompt` option will set the CALIENDO_PROMPT environment
variable so that you may use the interactive prompt built in caliendo.s

    $ py.test --caliendo --caliendo-prompt

\* This requires the --caliendo option to be present*
