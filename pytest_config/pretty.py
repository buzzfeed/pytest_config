import sys

SYSTEM = 0
RED = 31
GREEN = 32
YELLOW = 33

CHECK_MARK = u'\u2713'


def colorize_text(text, color=SYSTEM, bold=False):
    base_text = '\033[{bold};{color}m{text}\033[0m'
    if isinstance(text, unicode):
        base_text = unicode(base_text)
    color = (color, 1)[bold and color == SYSTEM]
    return base_text.format(bold=int(bold), color=color, text=text)


def print_color(args, color=SYSTEM, bold=False, new_line=True):
    for arg in args:
        print colorize_text(arg, color=color, bold=bold),
    if new_line:
        print '\n',
    sys.stdout.flush()


print_success = lambda *args, **kwargs: print_color(args, color=GREEN, **kwargs)
print_warning = lambda *args, **kwargs: print_color(args, color=YELLOW, **kwargs)
print_error = lambda *args, **kwargs: print_color(args, color=RED, **kwargs)


def formatwarning(message, category, filename, lineno, file_=None, line=None):
    s =  colorize_text("\n%s: %s\n" % (category.__name__, message), color=YELLOW)
    return s
