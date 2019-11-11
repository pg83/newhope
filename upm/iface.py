import sys
import imp
import itertools
import weakref


class IFace(object):
    def __init__(self):
        self._c = {}
        self._l = []
        self._a = {}
        self._cc = {}
        self._hit = 0
        self.add_lookup(lambda x: sys.modules[x])
        self.add_lookup(lambda x: self.find_module(x))
        self.add_lookup(lambda x: self.find_module('ya.' + x))
        self.add_lookup(lambda x: self.find_module('gn.' + x))
        self.add_lookup(self.fast_search)
        self.add_lookup(self.find_function)
        self.add_lookup(lambda x: __import__(x))

    def print_stats(self):
        for i, f in enumerate(self._l):
            print i, self._cc[i]

        print 'hit = ', self._hit, 'miss = ', len(self._c)

    def find_module(self, x):
        return __loader__._by_name[x]

    def fast_search(self, name):
        return __loader__._by_name[self._a[name]][name]

    def reindex_module(self, mod):
        def do():
            for x in frozenset(dir(mod)) - frozenset(dir(mod.__class__)):
                if x.startswith('__'):
                    continue

                yield x

        for k in do():
            self._a[k] = mod.__name__

    def find(self, name):
        subst = {
            'xpath': 'run_xpath_simple'
        }

        name = subst.get(name, name)

        for i, f in enumerate(self._l):
            try:
                ret = f(name)
                self._cc[i] += 1

                return ret
            except AttributeError:
                pass
            except KeyError:
                pass
            except ImportError:
                pass
            
        raise AttributeError(name)

    def __getattr__(self, name):
        try:
            self._hit += 1
            return self._c[name]
        except KeyError:
            self._hit -= 1
            self._c[name] = self.find(name)

        return self._c[name]

    def add_lookup(self, func):
        self._cc[len(self._l)] = 0
        self._l.append(func)

    def lookup(self, func):
        self.add_lookup(func)

        return func

    def print_cache(self):
        print self._c

    def find_function(self, name):
        for k in __loader__._order:
            m = __loader__._by_name[k]

            try:
                return m[name]
            except:
                pass

        raise AttributeError(name)


y = IFace()

        
def prompt(l):
   try:
      if l in y.verbose:
         frame = y.inspect.currentframe()
         frame = frame.f_back
         
         y.code.interact(local=frame.f_globals)
   except Exception as e:
      pass


script_path = sys.modules['__main__'].__file__
