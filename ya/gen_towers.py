ic = y.inc_counter()


@y.singleton
def is_debug():
    return 'debug' in y.config.get('tow', '')


@y.cached
def subst_by_platform(os):
    common = {
        'intl': 'gettext',
        'iconv': 'libiconv',
        'c++': 'libcxx',
        'm4': 'gnu-m4',
        'termcap': 'ncurses',
        'ncurses': 'ncurses-real',
    }

    by_os = {
        'linux': common.copy(),
        'darwin': common.copy(),
    }

    by_os['linux'].update({'ncurses': 'netbsd-curses'})
    by_os['linux'].update({'libtool': 'slibtool'})
    by_os['linux'].update({'m4': 'quasar-m4'})

    res = y.dc(by_os[os])

    for k in list(res.keys()):
        for s in y.repacks_keys():
            res[k + '-' + s] = res[k] + '-' + s

    return res


class Func(object):
    @y.cached_method
    def do_subst(self, x):
        s = subst_by_platform(self.data.info['os'])

        x = s.get(x, x)
        x = s.get(x, x)

        return x

    def __init__(self, x, data):
        self.x = x
        self.inc_count = ic()
        self.data = data
        self.i = 0

    def out_deps(self):
        y.info('{dr}' + str(self) + '{}', '->', '(' + ', '.join([str(self.data.func_by_num[i]) for i in self.deps]) + ')')

    def contains(self):
        return self.code().get('meta', {}).get('contains', [])

    def undeps(self):
        return self.raw_depends('undeps')

    @property
    def __name__(self):
        return str(self)

    def __str__(self):
        def iter_parts():
            if self.gen:
                yield self.gen

            yield self.base
            yield str(self.i)
            yield self.compact_kind() + self.data.info['os'][:1]


        return '<' + '-'.join(iter_parts())+ '>'

    def compact_kind(self):
        res = ''

        if self.is_tool:
            res += 't'

        if self.is_library:
            res += 'l'

        if not res:
            return 'u'

        return res

    @property
    def is_library(self):
        return 'library' in self.kind

    @property
    def is_tool(self):
        return 'tool' in self.kind

    @property
    def kind(self):
        return self.x['kind']

    @y.cached_method
    def code(self):
        return self.x['code']()

    @property
    def base(self):
        return self.x['base']

    @y.cached_method
    def raw_depends(self, name):
        code = self.code()

        if code:
            for x in self.code().get('meta', {}).get(name, []):
                yield self.do_subst(x)

    def depends(self):
        return list(self.raw_depends('depends'))

    @y.cached_method
    def all_depends(self):
        def it():
            for x in self.depends():
                yield x
                yield from self.data.by_name[x].all_depends()

        return frozenset(it())

    @y.cached_method
    def dep_lib_list(self):
        def iter():
            for x in self.dep_list():
                if self.data.by_name[x].is_library:
                    yield x

        return frozenset(iter())

    @y.cached_method
    def dep_tool_list(self):
        def iter():
            for x in self.dep_list():
                if not self.data.by_name[x].is_library:
                    yield x

        return frozenset(iter())

    def extra_libs(self):
        return self.data.extra_libs()

    @y.cached_method
    def dep_list(self):
        def iter1():
            yield from self.depends()
            yield from self.extra_libs()

        return frozenset(iter1()) - frozenset(self.undeps())

    @y.cached_method
    def run_func(self):
        data = y.dc(self.c())
        data['deps'] = y.uniq_list_x(data['deps'] + self.data.calc(self.deps))
        data['node']['codec'] = self.codec

        y.apply_meta(data['node']['meta'], y.join_metas([y.restore_node_node(d).get('meta', {}) for d in data['deps']]))

        return y.fix_pkg_name(data, self.z)

    @y.cached_method
    def c(self):
        return y.to_v2(self.code(), self.data.info)

    @property
    def f(self):
        return self.ff

    @property
    def z(self):
        return self.zz

    @y.cached_method
    def ff(self):
        return y.gen_func(self.run_func)

    @property
    @y.cached_method
    def zz(self):
        return {
            'code': self.ff,
            'base': self.base,
            'gen': self.gen,
            'kind': self.kind,
            'repacks': {},
            'info': self.data.info,
        }

    def clone(self):
        return Func(self.x, self.data)

    def calc_deps(self):
        if self.base == 'box':
            extra = []
        else:
            bg = self.data.box_by_gen.get(self.g - 1)

            if not self.data.flat:
                if bg is None:
                    extra = []
                else:
                    extra = [bg.i]
            else:
                extra = []

        return self.data.optimize(self.data.select_deps(self.base) + extra)


class SplitFunc(Func):
    def __init__(self, func, split):
        self._func = func
        self._split = split
        self.i = 0

    @property
    def gen(self):
        return self._func.gen

    @property
    def data(self):
        return self._func.data

    @property
    def kind(self):
        return self._func.kind + [self._split]

    def depends(self):
        return [self._func.base]

    def contains(self):
        return []

    def undeps(self):
        return ['musl', 'mimalloc', 'make']

    @y.cached_method
    def ff(self):
        return y.pkg_splitter(self._func.zz, self._split)()

    @property
    def base(self):
        return self._func.base + '-' + self._split

    def clone(self):
        return SplitFunc(self._func.clone(), self._split)

    @property
    @y.cached_method
    def zz(self):
        return {
            'code': self.ff,
            'base': self.base,
            'gen': self.gen,
            'kind': self.kind,
            'repacks': {},
            'info': self.data.info,
        }

class AllFunc(Func):
    def __init__(self, deps, data):
        def func():
            return {
                'meta': {
                    'depends': deps
                },
            }

        x = {
            'kind': ['all'],
            'code': func,
            'base': 'all',
        }

        self.gen = 'all'

        Func.__init__(self, x, data)


class Solver(object):
    def __init__(self, data, generation=0, seed=1):
        self._generation = generation
        self._data = data
        self._seed = seed
        self._r, self._w = y.make_engine(self._data, ntn=lambda x: x.base, dep_list=lambda x: x.dep_list(), seed=self._seed)
        self.inc_count = ic()

    def next_solver(self):
        return Solver(self._data, generation=(self._generation + 1), seed=(self._seed * 13 + 17))

    def iter_items(self):
        y.info('run solver')

        for el in self._r():
            self._w(el['i'])
            yield el['x']

        y.info('done')


class SolverWrap(object):
    def __init__(self, data):
        self._cur = Solver(data)

    def iter_solvers(self):
        while True:
            yield self._cur
            self._cur = self._cur.next_solver()

    def iter_infinity(self):
        for s in self.iter_solvers():
            for i in s.iter_items():
                yield i.clone()

    def generation(self):
        return self._cur._generation


class Data(object):
    def __init__(self, distr, info, flat, data):
        self.flat = flat
        self.info = info
        self.distr = distr
        self.new_funcs = []
        self.by_name = {}
        self.box_by_gen = {}
        self.dd = y.collections.defaultdict(list)
        self.func_by_num = []
        self.inc_count = ic()

        def iter_objects():
            for x in sorted(data, key=lambda x: x['base']):
                res = self.create_object(x)

                y.info('will gen func', res.base)

                yield res

        self.data = list(iter_objects())
        self.by_name['all'] = AllFunc(self.distr, self)

    def extra_libs(self):
        def do():
            yield 'make'
            yield 'busybox'

            if self.info.get('libc') == 'musl':
                yield 'musl'

            if self.info.get('libc') == 'uclibc':
                yield 'uclibc'

        return list(do())

    def create_object(self, x):
        return Func(x, self)

    def optimize(self, deps):
        def it():
            for i in deps:
                yield from self.func_by_num[i].contains()

        contains = frozenset(it())

        def iter_deps():
            for d in deps:
                f = self.func_by_num[d]

                if f.is_library:
                    yield d
                elif f.base in contains:
                    pass
                else:
                    yield d

        return frozenset(iter_deps())

    def last_elements(self, lst, must_have=True):
        def iter():
            for k in lst:
                if k in self.dd or must_have:
                    yield self.dd[k][-1]

        return list(iter())

    def prepare_funcs(self, num):
        solver = SolverWrap(self.data)
        pg = -1

        for func in solver.iter_infinity():
            g = solver.generation()

            if pg != g:
                self.calc_new_deps(g)
                pg = g

            if g >= num:
                break

            if g == num - 1:
                func.gen = ''
            else:
                func.gen = 'tow' + str(g)

            self.add_func(func, g)

            for k in y.repacks_keys():
                self.add_func(SplitFunc(func, k), g)

        self.add_func(self.by_name['all'], g)
        self.calc_new_deps(g)

    def calc_new_deps(self, g):
        for func in self.new_funcs:
            func.deps = sorted(func.calc_deps(), key=lambda x: -x)

        self.new_funcs = []

    def add_func(self, func, g):
        if func.base == 'box':
            self.box_by_gen[g] = func

        func.g = g
        self.new_funcs.append(func)
        self.by_name[func.base] = func
        func.i = len(self.func_by_num)
        self.func_by_num.append(func)
        self.dd[func.base].append(func.i)
        func.codec = 'pg'

    def find_first(self, name):
        return self.dd.get(name, [-1])[0]

    def register(self):
        v = self.func_by_num[-1]
        yield {'func': v.z}

    def iter_deps(self):
        for f in self.func_by_num:
            for d in f.deps:
                yield f.i, d

    def exec_seq(self):
        return list(y.execution_sequence(self.iter_deps()))

    def out(self):
        for x in self.func_by_num:
            x.out_deps()

        y.info('{bg}exec sequence', self.exec_seq(), '{}')

    def full_deps(self, name):
        return self.full_lib_deps(name) | self.full_tool_deps(name)

    @y.cached_method
    def full_lib_deps(self, name):
        my_deps = self.by_name[name].dep_lib_list()

        def iter_lst():
            for y in my_deps:
                yield y
                yield from self.full_lib_deps(y)

        return frozenset(iter_lst())

    @y.cached_method
    def full_tool_deps(self, name):
        return frozenset(self.by_name[name].dep_tool_list())

    def find_func(self, name):
        return self.by_name[name]

    def select_deps(self, name):
        return self.last_elements(self.full_deps(name))

    @y.cached_method
    def calc(self, deps):
        return [self.func_by_num[d].f() for d in deps]


class Tower(object):
    def __init__(self, distr, cc, flat):
        self._distr = distr
        self._data = []
        self._cc = cc
        self._flat = flat

    def on_data(self, data):
        y.info('will gen func for', data['base'])
        self._data.append(data)

    def gen_funcs(self):
        dt = Data(self._distr, self._cc, self._flat, [x for x in self._data])
        dt.prepare_funcs(3)
        dt.out()

        cnt = 0

        try:
            for x in dt.register():
                cnt += 1
                yield x
        except IndexError:
            pass

        if not cnt:
            y.error('{br}no package detected in', self._cc, '{}')
