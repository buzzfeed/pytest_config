__version__ = '0.0.3'

import ConfigParser
import os
import subprocess
import sys

CONFIG_SECTION = 'pytest_config'
DIR = os.path.dirname(os.path.realpath(__file__))

SYSTEM = 0
RED = 31
GREEN = 32
YELLOW = 33


def _print_color(args, color=SYSTEM, bold=False, new_line=True):
    base_text = '\033[{bold};{color}m{text}\033[0m'
    if bold and color == SYSTEM:
        color = 1
    params = {'bold': int(bold), 'color': color}
    for arg in args:
        params['text'] = arg
        print (base_text.format(**params)),
    if new_line:
        print '\n',
    sys.stdout.flush()


_print_success = lambda *args, **kwargs: _print_color(args, color=GREEN, **kwargs)
_print_warning = lambda *args, **kwargs: _print_color(args, color=YELLOW, **kwargs)
_print_error = lambda *args, **kwargs: _print_color(args, color=RED, **kwargs)

_get_template = lambda name: os.path.join(DIR, '_templates', name)


def add_project_to_pytest_path():
    """
    Pytest overwrites sys.path and messes up pytest-django.
    This function will check if the current project is in the path and will
    add it if it isn't already.
    """
    project_wsgi = subprocess.check_output('ls */wsgi.py', shell=True).replace('\n', '')
    project_name = project_wsgi.replace('/wsgi.py', '')

    # Verify setup.py exists. Create one otherwise.
    if not os.path.exists('setup.py'):
        print 'Installing setup.py...',
        setuppy_template_path = _get_template('setup.py')
        with open(setuppy_template_path) as setuppy_template:
            template_content = setuppy_template.read()
        template_content = template_content.format(project_name=project_name)
        with open('setup.py', 'w') as setuppy_file:
            setuppy_file.write(template_content)
        _print_success(' [OK]')

    # Check if project is installed
    print 'Checking if project is in py.test path...',
    cmd = 'pip install --no-install --no-download %s > /dev/null'
    return_value = subprocess.call(cmd % project_name, shell=True)
    if return_value != 0:  # already installed
        _print_error('[NOT IN PATH]')
        _print_warning('Adding project to py.test path...', new_line=False)
        subprocess.call('pip install -e . > /dev/null', shell=True)
        _print_success(' [OK]')
    else:
        _print_success(' [ALREADY IN PATH]')

    # Add project.egg to gitignore
    if not os.path.exists('.gitignore'):
        subprocess.call('touch .gitignore', shell=True)
    return_value = subprocess.call('cat .gitignore | grep .egg > /dev/null', shell=True)
    if return_value != 0:
        subprocess.call('echo "*.egg*" >> .gitignore', shell=True)

    _print_success('[SUCESS] You can now run your tests with py.test', bold=True)


def update_confg_version(template_paths, name):
    pytestini = ConfigParser.ConfigParser()
    try:
        with open(template_paths['pytest.ini']['dest']) as current:
            pytestini.readfp(current)
            if not pytestini.has_section(CONFIG_SECTION):
                pytestini.add_section(CONFIG_SECTION)
            pytestini.set(CONFIG_SECTION, '%s_version' % name, __version__)
    except IOError:
        _print_error('ERROR: Unable to set the current version of', name,
                     '. Please make sure you have a pytest.ini and try again.')
        sys.exit(1)
    with open(template_paths['pytest.ini']['dest'], 'w') as current:
        pytestini.write(current)
    print '[pytest_config] Updated version of', name, 'to', __version__
