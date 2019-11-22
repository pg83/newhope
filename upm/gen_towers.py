@y.defer_constructor
def init():
    @y.gd_callback('build env')
    def solver(arg):
        arg['back_channel']({'func': lambda info: {}, 'descr': ['system', 'fast']})


@y.singleton
def func_channel():
    return y.GEN_DATA_LOOP.write_channel('orig functions', 'ygg')


ic = y.inc_counter()


class Func(object):
    def __init__(self, x, data):
        self.x = x
        self.inc_count = ic()
        self.data = data
        self.i = 0

    def out_deps(self):
        y.xprint_dg(self.base, self.i, self.deps)

    @property
    def is_library(self):
        return 'library' in self.kind

    @property
    def is_tool(self):
        return 'tool' in self.kind

    @property
    def kind(self):
        return self.x['kind']

    @property
    def code(self):
        return self.x['code']

    @property
    def base(self):
        return self.x['base']

    def depends(self):
        return self.code().get('meta', {}).get('depends', [])

    def dep_lib_list(self):
        def iter():
            for x in self.dep_list():
                if self.data.by_name[x].is_library:
                    yield x

        return list(iter())

    def dep_tool_list(self):
        def iter():
            for x in self.dep_list():
                y = self.data.by_name[x]
                
                if y.is_tool or not y.is_library:
                    yield x
                    
        return list(iter())

    @y.cached_method
    def dep_list(self):
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

    @y.cached_method
    def run_func(self, info):
        data = y.deep_copy(self.c(info))
        data['deps'] = list(y.uniq_list_0(data['deps'] + self.data.calc(self.deps, info)))

        return y.fix_pkg_name(data, self.z)

    @y.cached_method
    def c(self, info):
        return y.to_v2(self.code(), info)

    @y.cached_method
    def f(self, info):
        return self.ff(info)
    
    @property
    @y.cached_method
    def z(self):
        return self.zz
    
    @y.cached_method
    def ff(self, info):
        return y.gen_func(self.run_func, info)

    @property
    @y.cached_method
    def zz(self):
        return {
            'code': self.ff,
            'base': self.base,
            'gen': 'tow',
            'kind': self.kind,
        }

    def clone(self):
        return Func(self.x, self.data)

    def calc_deps(self):
        return self.data.select_deps(self.base) + self.data.last_elements(self.data.special, must_have=False)


class SpecialFunc(Func):
    def __init__(self, x, data):
        Func.__init__(self, x, data)

    def depends(self):
        return self.data.by_kind[self.base]

    @y.cached_method
    def f(self, info):
        return self.z['code'](info)
    
    @property
    @y.cached_method
    def z(self):
        return {
            'code': y.pkg_splitter(self.zz, 'run'),
            'base': self.base,
            'gen': 'tow',
            'kind': self.kind + ['split', 'run'],
        }

    @y.cached_method
    def gen_c(self):
        return y.join_funcs(lambda info: self.data.calc(self.deps, info))

    @y.cached_method
    def c(self, info):
        return y.restore_node(self.gen_c()(info))

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
        self.wc = y.GEN_DATA_LOOP.write_channel('new functions', 'tow')
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
        return self.full_lib_deps(name) | self.full_tool_deps(name)

    @y.cached_method
    def full_lib_deps(self, name):
        my_deps = self.by_name[name].dep_lib_list()

        def iter_lst():
            for x in my_deps:
                yield x

            for y in my_deps:
                for x in self.full_lib_deps(y):
                    yield x

        return frozenset(iter_lst())

    def full_tool_deps(self, name):
        return frozenset(self.by_name[name].dep_tool_list())

    def select_deps(self, name):
        return self.last_elements(self.full_deps(name))

    @y.cached_method
    def calc(self, deps, arg):
        return [self.func_by_num[d].f(arg) for d in deps]


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
