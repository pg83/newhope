@y.defer_constructor
def init():
    @y.read_callback('build env', 'tow')
    def solver(arg):
        arg['back_channel']({'func': lambda info: {}, 'descr': ['system', 'fast']})


@y.singleton
def func_channel(): 
    return y.write_channel('orig functions', 'ygg')


ic = y.inc_counter()


class DictProxy(object):
    def __init__(self, x):
        self._x = x

    def __getitem__(self, n):
        return self._x.__getitem__(n)

    def get(self, k, v=None):
        return self._x.get(k, v)


@y.cached(key=lambda x, z: z)
def run_cached(f, key):
    return f()


class Func(object):
    def __init__(self, x, data):
        self.x = x
        self.inc_count = ic()
        self.data = data
        self.i = 0
            
    def out_deps(self):
        print self.base, self.i, self.deps

    def fun(self, i):
        return self.data.func_by_num[i].f

    def func_apply(self, i, x):
        return self.data.func_by_num[i].f(x)

    @property
    def code(self):
        return self.x['code']

    @property
    def base(self):
        return self.x['base']

    def depends(self):
        return self.code().get('meta', {}).get('depends', [])

    def dep_list(self):
        return run_cached(self.dep_list_base, [self.inc_count, 'self.dep_list_base'])

    def dep_list_base(self):
        subst = {
            'intl': 'gettext',
            'iconv': 'libiconv',
        }

        def iter1():
            yield 'make'
                
            for y in self.depends():
                yield subst.get(y, y)

        def iter2():
            for y in iter1():
                if y != self.base:
                    yield y

        return list(iter2())

    def run_func(self, info):
        def func():
            data = y.deep_copy(self.c(info))

                #if not data.get('deps'):
            data['deps'] += [self.func_apply(d, info) for d in self.deps]

            return y.fix_pkg_name(data, self.z)
            
        return run_cached(func, [self.inc_count, 'self.run_func', info])

    def c(self, info):
        def func():
            return y.to_v2(self.code(), info)

        return run_cached(func, [self.inc_count, 'self.c', info])

    def f(self, info):
        def func():
            return y.gen_func(self.run_func, info)

        return run_cached(func, [self.inc_count, 'self.f', info])

    @property
    def z(self):
        def func():
            return {
                'code': self.f,
                'base': self.base,
                'gen': 'tow',
                'kind': ['tow'],
            }

        return run_cached(func, [self.inc_count, 'self.z', 'func'])

    def clone(self):
        return Func(self.x, self.data)

    def calc_deps(self):
        return self.data.select_deps(self.base) + self.data.last_elements(self.data.special, must_have=False)


class SpecialFunc(Func):
    def __init__(self, x, data):
        Func.__init__(self, x, data)

    def depends(self):
        return self.data.by_kind[self.base]

    def gen_c(self):
        def join():
            return y.join_funcs([self.fun(d) for d in self.deps])

        return run_cached(join, [self.inc_count, 'self.gen_cx', 'join'])

    def c(self, info):
        def call_c():
            return y.restore_node(self.gen_c()(info))

        return run_cached(call_c, [self.inc_count, 'self.cx', 'call_c'])

    def clone(self):
        return SpecialFunc(self.x, self.data)

    def calc_deps(self):
        return self.data.last_elements(self.depends())


class Solver(object):
    def __init__(self, data, seed=1):
        self._data = data
        self._seed = seed
        self._r, self._w = y.make_engine(self._data, ntn=lambda x: x.base, dep_list=lambda x: x.dep_list(), seed=self._seed)
        self.inc_count = ic()

    def next_solver(self):
        return Solver(self._data, self._seed * 13 + 17)

    def iter_items(self):
        for el in self._r():
            self._w(el['i'])
            yield el['x']
                
    def iter_solvers(self):
        cur = self

        while True:
            yield cur
            cur = cur.next_solver()

    def iter_infinity(self):
        for s in self.iter_solvers():
            for i in s.iter_items():
                yield i.clone()


class Data(object):
    def __init__(self, data):
        self.by_kind = y.collections.defaultdict(list)
        
        for x in data:
            for k in x['func']['kind']:
                self.by_kind[k].append(x['func']['base'])

        self.dd = y.collections.defaultdict(list)
        self.func_by_num = []
        self.wc = y.write_channel('new functions', 'tow')
        self.inc_count = ic()
        self.data = [self.create_object(x['func']) for x in data]
        self.by_name = dict((x.base, x) for x in self.data)

    def create_object(self, x):
        if x['base'] in self.special:
            return SpecialFunc(x, self)

        return Func(x, self)

    @property
    def special(self):
        return self.by_kind['special']

    def last_elements(self, lst, must_have=True):
        def iter():
            for k in lst:
                if k in self.dd or must_have:
                    yield self.dd[k][-1]
                    
        return list(iter())

    def prepare_funcs(self, num):
        solver = Solver(self.data)

        for func in solver.iter_infinity():
            func.i = len(self.func_by_num)
            self.func_by_num.append(func) 
            func.deps = func.calc_deps()
            self.dd[func.base].append(func.i)

            if func.i > num:
                break

    def register(self):
        for v in self.func_by_num:
            self.wc({'func': v.z})

    def out(self):
        for x in self.func_by_num:
            x.out_deps()

    def full_deps(self, name):
        def func():
            my_deps = self.by_name[name].dep_list()

            if not my_deps:
                return []

            def iter_lst():
                yield my_deps

                for y in my_deps:
                    yield self.full_deps(y)

            return sorted(frozenset(sum(iter_lst(), [])))

        return run_cached(func, [self.inc_count, 'self.full_deps', name])
            
    def select_deps(self, name):
        return self.last_elements(self.full_deps(name))


def make_proper_permutation(data):
    dt = Data(data)
    dt.prepare_funcs(150)
    dt.register()
    #dt.out()


@y.ygenerator(tier=0)
def box0():
    return {
        'meta': {
            'kind': ['special', 'tool'],
        },
    }


@y.ygenerator(tier=0)
def compression0():
    return {
        'meta': {
            'kind': ['special', 'tool'],
        },
    }


def make_perm():
    make_proper_permutation(y.original_funcs())
