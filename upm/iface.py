import sys
import imp


def my_modules():
    for path in sorted(sys.builtin_modules['upm'].keys()):
        name, _ = sys.builtin_modules['upm'][path]

        yield name, sys.modules[name]


def find_function(name):
    subst = {
        'xpath': 'run_xpath_simple'
    }

    for _, m in my_modules():
        if name in m.__dict__:
            return m.__dict__[name]

    try:
        return sys.modules['upm_' + name]
    except KeyError:
        pass

    try:
        return __import__(name)
    except ImportError:
        pass

    raise AttributeError(name)


class IFace(object):
    def __init__(self):
        self._c = {}

    def __getattr__(self, name):
        if name not in self._c:
            self._c[name] = find_function(name)

        return self._c[name]


y = IFace()
