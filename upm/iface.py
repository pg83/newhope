import sys
import imp
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


def find_function(name):
    subst = {
        'xpath': 'run_xpath_simple'
    }

    name = subst.get(name, name)

    for m in my_modules().values():
        if name in m.__dict__:
            return m.__dict__[name]

    raise AttributeError(name)


class IFace(object):
    def __init__(self):
        self._c = {}

    def __getattr__(self, name):
        if name not in self._c:
            self._c[name] = find_function(name)

        return self._c[name]


y = IFace()
