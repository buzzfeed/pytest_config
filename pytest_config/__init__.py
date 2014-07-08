__version__ = '0.0.9'

import ConfigParser
import os
import subprocess
from . import pretty

CONFIG_SECTION = 'pytest_config'
DIR = os.path.dirname(os.path.realpath(__file__))

_get_template = lambda name: os.path.join(DIR, '_templates', name)


def add_project_to_pytest_path():
    """
    Pytest overwrites sys.path and messes up pytest-django.
    This function will check if the current project is in the path and will
    add it if it isn't already.
    """
    project_wsgi = subprocess.check_output('ls */wsgi.py',
                                           shell=True).replace('\n', '')
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
        pretty.print_success(' [OK]')

    # Check if project is installed
    cmd = 'pip install --no-install --no-download %s > /dev/null'
    if subprocess.call(cmd % project_name, shell=True):  # already installed
        pretty.print_warning('Adding project to pytest-django path...',
                              new_line=False)
        subprocess.call('pip install -e . > /dev/null', shell=True)
        pretty.print_success(' [OK]')
    else:
        success_message = 'Project is already available for pytest-django!'
        pretty.print_success(pretty.CHECK_MARK, success_message)

    # Add project.egg to gitignore
    if not os.path.exists('.gitignore'):
        subprocess.call('touch .gitignore', shell=True)
    cmd = 'cat .gitignore | grep *.egg-info > /dev/null'
    if subprocess.call(cmd, shell=True):  # not in .gitignore
        subprocess.call('echo "*.egg-info" >> .gitignore > /dev/null', shell=True)

    success_message = 'You can now run your tests with py.test'
    pretty.print_success(pretty.CHECK_MARK, success_message)


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
