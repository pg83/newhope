import sys
import imp
import threading
import inspect


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

    def lst(self):
        return (self.find_module, self.find_function)
    
    def find(self, name):
        for f in self.lst():
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

    
class IFaceStd(IFaceSlave):
    def __init__(self, mod, parent):
        IFaceSlave.__init__(self, mod, parent)

    def import_from(self, name):
        ctx = dict()
        exec('from ' + self._mod.__name__ + ' import ' + name, ctx)
        return ctx[name]
        
    def find_module_1(self, name):
        return self._pa.create_std(__import__(self._mod.__name__ + '.' + name))

    def find_module_2(self, name):
        x = self.import_from(name)

        if inspect.ismodule(x):
            return self._pa.create_std(x)

        raise AttributeError(name)

    def find_module_3(self, name):
        x = self._mod.__dict__[name]
        
        if inspect.ismodule(x):
            return self._pa.create_std(x)

        raise AttributeError(name)
        
    def find_function_1(self, name):
        return self._mod.__dict__[name]
    
    def find_function_2(self, name):
        return self.import_from(name)

    def lst(self):
        return (self.find_module_2, self.find_module_1, self.find_module_3, self.find_function_1, self.find_function_2)

    
stdio_lock = threading.Lock()
    

class StdIO(object):
    def __init__(self, s):
        self.s = s

    def write(self, t):
        with stdio_lock:
            self.s.buffer.write(t.encode('utf-8'))
            self.s.buffer.flush()
        
    def flush(self):
        with stdio_lock:
            self.s.flush()
        
        
class ColorStdIO(object):
    def __init__(self, s):
        self.s = s
        self.p = ''

    def colorize(self, t):
        try:
            if 'debug' in y.config.get('color', ''):
                return t
        except Exception:
            pass
        
        if len(t) < 100000:
            try:
                return y.process_color(t, '', {})
            except AttributeError as e:
                pass
            except Exception as e:
                print e

        return t

    def get_part(self):
        try:
            return self.p
        finally:
            self.p = ''
                
    def write(self, t):
        if not t:
            return
        
        with stdio_lock:
            if len(t) > 4096:
                self.flush_impl()
                self.write_part(t)
            else:
                self.p += t

                if len(self.p) > 4096:
                    self.flush_impl()

    def write_part(self, p):
        if p:
            try:
                self.s.buffer.write(self.colorize(p).encode('utf-8'))
            except AttributeError:
                self.s.buffer.write(p)
                
        self.s.buffer.flush()
        self.s.flush()

    def flush_impl(self):
        self.write_part(self.get_part())
        
    def flush(self):
        with stdio_lock:
            self.flush_impl()
            

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
        self.add_lookup(lambda x: self.find_module('ut.' + x))
        self.add_lookup(lambda x: self.create_std(sys.modules[x]))
        self.add_lookup(self.fast_search)
        self.add_lookup(self.find_function)
        self.add_lookup(lambda x: self.create_std(__import__(x)))

    def spawn(self, coro, name=None):
        return self.async_loop.spawn(coro, name)
        
    async def offload(self, job):
        return await self.async_loop.offload(job)

    def print_tbx(self, *args, **kwargs):
        try:
            y.print_tbx_real(*args, **kwargs)
        except Exception:
            y.traceback.print_exc(chain=True)
      
    def last_msg(self, t):
        e = self.stderr
        o = self.stdout
        
        sys.stderr = None
        sys.stdout = None

        self.stderr = None
        self.stdout = None

        o.flush()
        e.write(t)
        e.flush()

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

    def create_slave_0(self, mod, klass):
        key = 's:' + mod.__name__ + ':' + klass.__name__

        try:
            return self[key]
        except KeyError:
            self[key] = klass(mod, self)

        return self[key]

    def create_slave(self, mod):
        return self.create_slave_0(mod, IFaceSlave)
    
    def create_std(self, mod):
        return mod
        #return self.create_slave_0(mod, IFaceStd)

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
            except KeyError:
                pass

        raise AttributeError(name)


y = IFace()
y.sys.modules['__main__'].y = y


def prompt(l):
    def can_use():
        try:
            if l in y.verbose:
                return True

            return y.config.get(l, False)
        except Exception as e:
            print(e)

        return False

    if can_use():
        frame = y.inspect.currentframe()
        frame = frame.f_back

        try:
            from ptpython.repl import embed

            embed(frame.f_globals, locals())
        except ImportError:
            y.code.interact(local=frame.f_globals)
        except Exception as e:
            y.debug('in prompt', e)

  
def load_builtin_modules(data, builtin):
    initial = (
        'ut.rng',
        'ut.mod_load',
        'ut.init_log',
        'ut.int_counter',
        'ut.args_parse',
        'ut.algo',
        'ut.single',
        'ut.at_exit',
        'ut.err_handle',      
        'ut.caches',
        'ut.pub_sub',
        'ut.defer',        
        'ut.manager',
        'ut.mini_db',
        'ut.queues',
        
        'ya.ygen',
        'ya.noid_calcer',
    )

    for m in initial:
        __loader__.create_module(m)

    initial = set(initial)
    
    for k in builtin:
        if k not in initial:
            if k.startswith('ya') or k.startswith('ut'):
                __loader__.create_module(k)
                initial.add(k)


def run_stage4_0(data):
    try:
        @y.lookup
        def lookup(name):
            return data[name]
        
        load_builtin_modules(y.file_data, y.builtin_modules)

        y.init_logger(log_level=y.config.get('ll', 'info').upper())

        y.debug('will run defer constructors')
        y.run_defer_constructors()
        y.debug('done')

        async def flush_streams():
            ctl = y.current_coro()
            
            while True:
                await ctl.sleep(0.1)

                try:
                    y.stdout.flush()
                    y.stderr.flush()
                except Exception as e:
                    y.debug('in flush streams', e)
        
        async def entry_point():
            try:
                try:
                    return await y.run_main(data.pop('args'))
                except SystemExit as e:
                    code = e.code
                    
                    if code is None:
                        code = 0

                    y.shut_down(retcode=code)
                except:
                    y.print_tbx()
                    y.shut_down(retcode=10)
            finally:
                y.shut_down(0)

        ctx1 = y.spawn(entry_point)
        ctx2 = y.spawn(flush_streams)
    except:
        y.os.abort()
