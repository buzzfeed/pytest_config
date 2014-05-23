# History

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
