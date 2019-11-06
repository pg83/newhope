import sys
import imp
import itertools


class IFace(object):
    def __init__(self):
        self._c = {}
        self._l = []

        self.add_lookup(lambda x: sys.modules[x])
        self.add_lookup(self.find_function)
        self.add_lookup(lambda x: __import__(x))

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
            except ImportError:
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

    def print_cache(self):
        print self._c

    def find_function(self, name):
        for m in itertools.chain(__loader__.iter_modules(), [sys.modules['__main__']]):
            if m.__name__ == name:
                return m

            try:
                return m.__dict__[name]
            except:
                pass

        raise AttributeError(name)


y = IFace()
