from .logger import logger
from . import pretty
import pytest


def _error(e):
    error = '{}: {}'.format(type(e).__name__, str(e))
    logger.debug(pretty.colorize_text(error, color=pretty.YELLOW))


@pytest.fixture
def timezone():
    from django.utils import timezone
    return timezone


@pytest.fixture
def pytz():
    import pytz
    return pytz


@pytest.fixture
def json():
    import json
    return json


@pytest.fixture
def mock():
    try:
        import mock
        return mock
    except ImportError as e:
        _error(e)


@pytest.fixture
def model_mommy():
    try:
        import model_mommy
        return model_mommy.mommy
    except ImportError as e:
        _error(e)
