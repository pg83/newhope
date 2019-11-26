import sys
import imp
import threading
import asyncio


class StopNow(Exception):
    pass


class IFaceSlave(dict):
    def __init__(self, mod, parent):
        self.__dict__ = self
        self._mod = mod
        self._pa = parent

    def __getattr__(self, name):
        key = self._mod.__name__ + '.' + name

        try:
            return self[key]
        except KeyError:
            self[key] = self.find(name)

        return self[key]

    def find(self, name):
        for f in (self.find_module, self.find_function):
            try:
                return f(name)
            except AttributeError:
                pass
            except KeyError:
                pass
            except ImportError:
                pass
            
        raise AttributeError(name)
        
    def find_module(self, name):
        return self._pa.create_slave(__loader__._by_name[self._mod.__name__ + '.' + name])

    def find_function(self, name):
        return self._mod[name]

    
stdio_lock = threading.Lock()
    

class StdIO(object):
    def __init__(self, s):
        self.s = s

    def write(self, t):
        with stdio_lock:
            self.s.write(t)
        
    def flush(self):
        with stdio_lock:
            self.s.flush()
        
        
class ColorStdIO(object):
    def __init__(self, s):
        self.s = s

    def write(self, t):
        if len(t) < 10000:
            try:
                t = y.process_color(t, '', {})
            except AttributeError:
                pass
                
        with stdio_lock:
            try:
                self.s.write(t)
            except TypeError:
                self.s.buffer.write(t)
                
    def flush(self):
        with stdio_lock:
            self.s.flush()

    def out(self, *args):
        #pass
        self.write(' '.join([str(x) for x in args]) + '\n')


class IFace(dict):
    def __init__(self):
        self.__dict__ = self
        self._l = []
        self._a = {}
        self._cc = {}
        self._hit = 0

        self.reset_stdio()
        
        self.add_lookup(lambda x: self.find_module(x))
        self.add_lookup(lambda x: self.find_module('ya.' + x))
        self.add_lookup(lambda x: self.find_module('gn.' + x))
        self.add_lookup(lambda x: self.find_module('pl.' + x))
        self.add_lookup(lambda x: sys.modules[x])
        self.add_lookup(self.fast_search)
        self.add_lookup(self.find_function)
        self.add_lookup(lambda x: __import__(x))
    
    @property
    def copy(self):
        try:
            return sys.modules['copy']
        except KeyError:
            __import__('copy')
            
        return sys.modules['copy']
        
    def reset_stdio(self):
        self.stdout = ColorStdIO(sys.stdout)
        self.stderr = ColorStdIO(sys.stderr)        
        
    def set_stdio(self, stdout=None, stderr=None):
        if stdout:
            self.stdout = StdIO(stdout)

        if stderr:
            self.stderr = StdIO(stderr)
        
    def print_stats(self):
        for i, f in enumerate(self._l):
            y.xprint_w(i, self._cc[i])

        y.xprint_w('hit =', self._hit, 'miss =', len(self._c))

    def create_slave(self, mod):
        key = 's:' + mod.__name__

        try:
            return self[key]
        except KeyError:
            self[key] = IFaceSlave(mod, self)

        return self[key]

    def find_module(self, x):
        return self.create_slave(__loader__._by_name[x])

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
            'xpath': 'run_xpath_simple',
            'Queue': 'queue',
            'thread': 'threading',
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
            return self[name]
        except KeyError:
            self._hit -= 1
            self[name] = self.find(name)

        return self[name]

    def add_lookup(self, func):
        self._cc[len(self._l)] = 0
        self._l.append(func)

    def lookup(self, func):
        self.add_lookup(func)

        return func

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

  
def load_builtin_modules(data, builtin):
    initial = (
        'ya.mod_load',
        'ya.int_counter',
        'ya.args_parse',
        'ya.algo',
        'ya.single',
        'ya.err_handle',      
        'ya.caches',
        'ya.pub_sub2',
        'ya.init_log',
        'ya.defer',
        'ya.pub_sub',
        'ya.ygen',
        'ya.manager',
        'ya.mini_db',
        'ya.noid_calcer',
    )

    for m in initial:
        __loader__.create_module(m)

    initial = set(initial)

    for k in builtin:
        if k not in initial:
            if k.startswith('ya'):
                __loader__.create_module(k)
                initial.add(k)


def run_stage4_1(data):
    @y.lookup
    def lookup(name):
        return data[name]
    
    load_builtin_modules(y.file_data, y.builtin_modules)

    data['signal_channel'] = y.get_signal_channel()

    y.debug('will run defer constructors')
    y.run_defer_constructors()
    y.debug('done')
    
    return y.run_main(data.pop('args'))


def to_int(v):
    if v is None:
        return 0
    
    return int(v)


def run_stage4_0(data):
    try:
        try:            
            y.os._exit(to_int(run_stage4_1(data)))
        except SystemExit as e:
            y.os._exit(e.code)            
        except:
            try:
                y.stderr.write(y.format_tbx() + '\n')
            except:
                y.stderr.write(y.traceback.format_exc() + '\n')
    finally:
        y.os.abort()
