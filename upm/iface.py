import sys


load_complete = False


def my_modules():
    for path in sorted(sys.builtin_modules['upm'].keys()):
        name, data = sys.builtin_modules['upm'][path]

        if name.startswith('upm'):
            yield name, sys.modules[name]


def find_function(name):
    if name == 'options':
        #from upm_decor import options
        #return options
        sys.modules['upm_decor'].__dict__['options']

    if name == 'wraps':
        from upm_ft import wraps

        return wraps

    subst = {
        'xpath': 'run_xpath_simple'
    }

    for _, m in my_modules():
        if name in m.__dict__:
            return m.__dict__[name]

    try:
        return __import__('upm_' + name)
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
