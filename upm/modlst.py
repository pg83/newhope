import sys
import importlib


def my_modules():
    def do():
        for name, text in sys.builtin_modules['upm'].iteritems():
            if name.startswith('upm'):
                yield name, importlib.import_module(name)

    try:
        my_modules.__res
    except AttributeError:
        my_modules.__res = dict(do())

    return my_modules.__res
