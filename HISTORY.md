# History

### 0.0.8 (2014-06-19)

* Cleanup and organization for releasing to PyPI.
* Added MANIFEST.in
* Moved `pytest_config.django` Django app to just `pytest_config`.

### 0.0.7 (2014-06-16)

* Added `--runslow` option to run tests marked as slow tests.
* Added `pytest-django` as package requirement since this is meant to be used
within Django projects.
* `pep8>=1.5.6` as package requirement as this version supports more PEP8 rules.

### 0.0.6 (2014-06-05)

* Fixed bug when detecting parsing DJANGO_SETTINGS_MODULE and checking
availability of such.

### 0.0.5 (2014-05-30)

* Added support for lowercase `django_settings_module` ini value in pytest.ini.
* Added `-y`, `--overwrite` to `pytest_config.update` that will make the script
automatically overwrite the user configurations with the defaults.
* Added `-p`, `--fix-path` to only fix the pytest-django known issue.
* `pretty._print_*` is now `pretty.print_*`.

### 0.0.4 (2014-05-22)

* Refactored `_print_color` to make text coloring function `colorize_text`
importable and reusable over apps using `pytest_config`.

### 0.0.3 (2014-05-15)

* Added `--fix-path-issues` option to inspect the current django project and
check whether the project is available in the `PYTHON_PATH` for `py.test`;
if not, add it to the pat by installing in via a simple `setup.py` file.
* Made `pytest_config.init` and `pytest_config.update` more verbose.

## 0.0.2 (2014-05-13)

* Added commands to initialize and interactively update the configuration files.
* Checking last version of configuration files before running the tests.
 * If no information of configuration files last version is available,
   print an error message and terminate tests execution until this information
   is available.
 * If the version seems outdated, print a warning suggesting the user to run
the updater command.

## 0.0.1 (2014-05-08)

* First release as having initial configurations.
* Caliendo-friendly command arguments available.
