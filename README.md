# pytest-config

Base configurations and utilities for developing your Python project test suite.

### Installation

    pip install git+git://github.com/buzzfeed/pytest_config.git@0.0.2#egg=pytest_config==0.0.2

This will install:

- the `py.test` plugin
- a simple django app that extends the `django-admin.py startapp` (under development).
- a `pytest_config.init` command to initialize new config files
- a `pytest_config.update` command to interactively update your config files
against the lates default values.

### Features

#### Config files management

###### pytest_config.init

This command will copy all the configuration files needed to easily configure
`py.test` and `coverage`. Beware of this command as **it will simply replace any
existing config files in you current directory**.

###### pytest_config.update

This command will read the default configuration files and your customized
configuration files. If any of the options in you custom configuration differs
from the defaults, you will be prompted if you want to keep the current one.
If you decline, the default will be saved to your local configuration.

The two previous command share their interface, which is as follows:

Print the help page.

    $ pytest_config.update -h

Silence the process so that you are prompted about anything.
The defaults will be applied if you use this.

    $ pytest_config.[init|update] [-q|--noinput]`

Make the command apply its operations only for the `.coveragerc` file.

    $ pytest_config.[init|update] --coverage`

Make the command apply its operations only for the `pytest.ini` file.

    $ pytest_config.[init|update] --pytest-ini`

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

The `--caliendo-purge` option will set the `CALIENDO_PURGE` environment variable
so that caliendo can get rid of unused cache/evs/etc.

    $ py.test --caliendo --caliendo-purge

###### --caliendo-prompt *

The `--caliendo-prompt` option will set the `CALIENDO_PROMPT` environment
variable so that you may use the interactive prompt built in caliendo.

    $ py.test --caliendo --caliendo-prompt

\* This requires the --caliendo option to be present*
