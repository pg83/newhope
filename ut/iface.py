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
        return self._pa.create_slave(self._mod.__sub__[name])

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


class IFace(dict):
    def __init__(self):
        self.__dict__ = self
        self._l = []
        self._a = {}
        self._cc = {}
        self._hit = 0
   
        self.add_lookup(self.fast_search)
        self.add_lookup(self.find_function)
        self.add_lookup(lambda x: self.find_module(x))
        self.add_lookup(lambda x: self.create_std(sys.modules[x]))
        self.add_lookup(lambda x: self.create_std(__import__(x)))

    def clear_cache(self):
        for k in list(self.keys()):
            if k.startswith('_'):
                continue

            self.pop(k)

    @property
    def stdout(self):
        return sys.stdout

    @property
    def stderr(self):
        return sys.stderr

    def spawn(self, coro, name=None, debug=True):
        return self.async_loop.spawn(coro, name=name, debug=debug)

    async def offload(self, job):
        return await self.async_loop.offload(job)
  
    def last_msg(self, t):
        e = sys.stderr
        o = sys.stdout

        sys.stderr = None
        sys.stdout = None

        o.flush()
        e.flush()

        e.write(t)
        e.flush()

    @property
    def copy(self):
        try:
            return sys.modules['copy']
        except KeyError:
            __import__('copy')

        return sys.modules['copy']

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
        y = '.' + x

        for mod in __loader__.iter_modules():
            if mod.__name__.endswith(y):
                return self.create_slave(mod)

        raise AttributeError(x)

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
        for m in __loader__.iter_modules():
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

  
def load_builtin_modules(builtin):
    initial = (
        'ut.burn_it',
        'ut.single',
        'ut.preproc',
        'ut.xprint',
        'ut.rng',
        'ut.mod_load',
        'ut.defer',
        'ut.std_io',
        'ut.init_log',
        'ut.int_counter',
        'ut.mini_db',
        'ut.args_parse',
        'ut.algo',
        'ut.at_exit',
        'ut.err_handle',  
        'ut.caches',
        'ut.pub_sub',
        'ut.cli',
        'ut.queues',
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
        run_stage4_1(data)
    except:
        y.os.abort()


def builtin_data(name):
    return y.globals.by_name[name]['data']


def run_stage4_1(data):
    @y.lookup
    def lookup(name):
        return data[name]

    y.clear_cache()
    y.linecache.clearcache()

    load_builtin_modules(y.globals.builtin_modules)

    data['async_loop'] = y.CoroLoop('main')

    y.init_logger(log_level=y.config.get('ll', 'info').upper())

    y.debug('will run defer constructors')
    y.run_defer_constructors()
    y.debug('done')

    async def flush_streams():
        ctl = y.current_coro()
        ss = [y.stderr, y.stdout]

        while True:
            try:
                for s in ss:
                    await ctl.sleep(0.1)
                    s.flush()
            except Exception as e:
                y.debug('in flush streams', e)

    async def entry_point():
        try:
            try:
                return await y.run_main(data.pop('args'))
            except AssertionError as e:
                print('{br}' + str(e) + '{}', file=y.stderr)
                y.shut_down(1)
            except SystemExit as e:
                code = e.code

                if code is None:
                    code = 0

                y.shut_down(retcode=code)
            except:
                y.os.abort()
        finally:
            y.shut_down(0)

    y.spawn(entry_point, debug=False)
    y.spawn(flush_streams, debug=False)
