import sys
import imp


def my_modules():
    for path in sorted(sys.builtin_modules['upm'].keys()):
        name, _ = sys.builtin_modules['upm'][path]

        yield name, sys.modules[name]


class IFace(object):
    def __init__(self):
        self._c = {}
        self._l = []

        self.add_lookup(lambda x: sys.modules['upm_' + x])
        self.add_lookup(lambda x: sys.modules[x])
        self.add_lookup(self.find_function)

    def find(self, name):
        subst = {
            'xpath': 'run_xpath_simple'
        }

        name = subst.get(name, name)

        for f in self._l:
            try:
                return f(name)
            except AttributeError:
                pass
            except KeyError:
                pass

        raise AttributeError(name)

    def __getattr__(self, name):
        if name not in self._c:
            self._c[name] = self.find(name)

        return self._c[name]

    def add_lookup(self, func):
        self._l.append(func)

    def lookup(self, func):
        self.add_lookup(func)

        return func

    def find_function(self, name):
        for _, m in my_modules():
            if name in m.__dict__:
                return m.__dict__[name]

        raise AttributeError(name)


y = IFace()
