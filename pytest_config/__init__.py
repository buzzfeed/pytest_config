__version__ = '0.0.10'

import ConfigParser
import os
from . import pretty

CONFIG_SECTION = 'pytest_config'
DIR = os.path.dirname(os.path.realpath(__file__))

_get_template = lambda name: os.path.join(DIR, '_templates', name)


def update_confg_version(template_paths, name):
    pytestini = ConfigParser.ConfigParser()
    try:
        with open(template_paths['pytest.ini']['dest']) as current:
            pytestini.readfp(current)
            if not pytestini.has_section(CONFIG_SECTION):
                pytestini.add_section(CONFIG_SECTION)
            pytestini.set(CONFIG_SECTION, '%s_version' % name, __version__)
    except IOError:
        pretty.print_error('ERROR: Unable to set current version of', name,
                     '. Please make sure you have a pytest.ini and try again.')
        raise SystemExit(1)
    with open(template_paths['pytest.ini']['dest'], 'w') as current:
        pytestini.write(current)
    print '[pytest_config] Updated version of', name, 'to', __version__
