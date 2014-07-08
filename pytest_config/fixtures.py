from .logger import logger
from . import pretty
import pytest


def _error(e):
    error = '{}: {}'.format(type(e).__name__, str(e))
    logger.debug(pretty.colorize_text(error, color=pretty.YELLOW))


@pytest.fixture(scope='module')
def timezone():
    """ A shortcut to the `django.utils.timezone` module. """
    from django.utils import timezone
    return timezone


@pytest.fixture(scope='module')
def pytz():
    """ A shortcut to the `pytz` module. """
    import pytz
    return pytz


@pytest.fixture(scope='module')
def json():
    """ A shortcut to the `json` module. """
    import json
    return json


@pytest.fixture(scope='module')
def mock():
    """
    A shortcut to the `mock` module. If mock is not installed,
    an error will be logged and no module will be available.
    """
    try:
        import mock
        return mock
    except ImportError as e:
        _error(e)


@pytest.fixture(scope='module')
def model_mommy():
    """
    A shortcut to the `model_mommy.mommy` module. If model_mommy is not
    installed, an error will be logged and no module will be available.
    """
    try:
        from model_mommy import mommy
        return mommy
    except ImportError as e:
        _error(e)
