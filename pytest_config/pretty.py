import sys

SYSTEM = 0
RED = 31
GREEN = 32
YELLOW = 33


def colorize_text(text, color=SYSTEM, bold=False):
    base_text = '\033[{bold};{color}m{text}\033[0m'
    color = (color, 1)[bold and color == SYSTEM]
    return base_text.format(bold=int(bold), color=color, text=text)


def _print_color(args, color=SYSTEM, bold=False, new_line=True):
    for arg in args:
        print colorize_text(arg, color=color, bold=bold),
    if new_line:
        print '\n',
    sys.stdout.flush()


_print_success = lambda *args, **kwargs: _print_color(args, color=GREEN, **kwargs)
_print_warning = lambda *args, **kwargs: _print_color(args, color=YELLOW, **kwargs)
_print_error = lambda *args, **kwargs: _print_color(args, color=RED, **kwargs)


def formatwarning(message, category, filename, lineno, file_=None, line=None):
    s =  colorize_text("\n%s: %s\n" % (category.__name__, message), color=YELLOW)
    return s
