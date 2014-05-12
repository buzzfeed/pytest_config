__version__ = '0.0.2'

import os
import sys

CONFIG_SECTION = 'pytest_config'
DIR = os.path.dirname(os.path.realpath(__file__))

SYSTEM = '0m'
RED = '31m'
GREEN = '32m'
YELLOW = '33m'


def print_color(args, color=SYSTEM, bold=False):
    colored_text = '\033[%(bold)s;%(color)s%(text)s\033[%(reset_color)s'
    params = {'bold': int(bold), 'color': color, 'reset_color': SYSTEM}
    for arg in args:
        params['text'] = arg
        print (colored_text % params),
    print '\n',
    sys.stdout.flush()


print_success = lambda *args: print_color(args, color=GREEN)
print_warning = lambda *args: print_color(args, color=YELLOW)
print_error = lambda *args: print_color(args, color=RED)

get_template = lambda name: os.path.join(DIR, '_templates', name + '.txt')
