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
        'm4': 'quasar-m4',
        'termcap': 'ncurses',
        'ncurses': 'ncurses',
    }

    by_os = {
        'linux': common.copy(),
        'darwin': common.copy(),
    }

    by_os['linux'].update({'ncurses': 'netbsd-curses'})

    return by_os[os]


class Func(object):
    def do_subst(self, x):
        s = subst_by_platform(self.data.info['host']['os'])

        x = s.get(x, x)
        x = s.get(x, x)

        return x

    def __init__(self, x, data):
        self.x = x
        self.inc_count = ic()
        self.data = data
        self.i = 0

    def out_deps(self):
        y.xprint_db('{dr}' + str(self) + '{}', '->', '(' + ', '.join([str(self.data.func_by_num[i]) for i in self.deps]) + ')')

    def contains(self):
        return self.code().get('meta', {}).get('contains', [])

    @property
    def __name__(self):
        return str(self)

    def __str__(self):
        return '<' + self.base + '-' + str(self.i) + '-' + self.compact_kind() + '-' + self.data.info['target']['os'] + '>'

    def compact_kind(self):
        res = ''

        if self.is_tool:
            res += 't'

        if self.is_library:
            res += 'l'

        return res

    @property
    def is_library(self):
        return 'library' in self.kind

    @property
    def is_tool(self):
        return 'tool' in self.kind

    @property
    def kind(self):
        return self.slice(self.x['kind']) or []

    def slice(self, data):
        y.platform_slice(data, self.data.info['target'])

    @y.cached_method
    def code(self):
        return self.slice(self.x['code']())

    @property
    def base(self):
        return self.x['base']

    @y.cached_method
    def raw_depends(self):
        code = self.code()

        if code:
            return [self.do_subst(x) for x in self.code().get('meta', {}).get('depends', [])]

        return []

    def depends(self):
        return self.raw_depends()

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
            print 'dep', self.__name__

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

            for d in self.extra_libs():
                if self.base in self.data.find_func(d).all_depends():
                    continue

                if self.base == d:
                    continue

                code = self.code()

                if not code:
                    continue

                if 'code' not in code:
                    continue

                yield d

        return frozenset(iter1())

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
            'gen': 'tow',
            'kind': self.kind,
            'repacks': {},
            'info': self.data.info,
        }

    def clone(self):
        return Func(self.x, self.data)

    def calc_deps(self):
        return self.data.optimize(self.data.select_deps(self.base) + self.data.last_elements(self.data.special, must_have=False))


class SpecialFunc(Func):
    def __init__(self, x, data):
        print 'special', x, data
        Func.__init__(self, x, data)

    def depends(self):
        return self.data.by_kind[self.base]

    @y.cached_method
    def contains(self):
        def it():
            for x in self.depends():
                yield x
                yield from self.data.by_name[x].contains()

        return frozenset(it())

    @y.cached_method
    def f(self):
        return self.z['code']()

    @property
    @y.cached_method
    def z(self):
        return {
            'code': y.pkg_splitter(self.zz, 'run'),
            'base': self.base,
            'gen': 'tow',
            'kind': self.kind + ['split', 'run'],
            'info': self.data.info,
            'repacks': {},
        }

    @y.cached_method
    def c(self):
        f = y.join_funcs(lambda: self.data.calc(self.deps), ex_code='(cd $IDIR/bin && (rm python* pydoc* || true)) 2> /dev/null')

        return y.restore_node(f())

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

    def iter_solvers(self, num):
        cur = self
        yield cur

        for i in range(0, num - 1):
            cur = cur.next_solver()
            yield cur

    def iter_infinity(self, num):
        for s in self.iter_solvers(num):
            for i in s.iter_items():
                yield i.clone()


class Data(object):
    def __init__(self, info, data):
        self.info = info

        self.dd = y.collections.defaultdict(list)
        self.func_by_num = []
        self.inc_count = ic()

        def iter_objects():
            for x in sorted(data, key=lambda x: x['func']['base']):
                obj = self.create_object(x['func'])

                print 'obj', obj, obj.code()

                if obj.code():
                    yield obj

        self.data = list(iter_objects())
        self.by_name = dict((x.base, x) for x in self.data)
        self.by_kind = y.collections.defaultdict(list)

        for x in self.data:
            for k in x.kind:
                self.by_kind[k].append(x.base)

    def extra_libs(self):
        tg = self.info['host']

        if tg['os'] == 'linux':
            return ('make', 'musl', 'bestbox')

        return ('make',)

    def create_object(self, x):
        print 'create', x

        if x['base'] in self.special:
            return SpecialFunc(x, self)

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

    @property
    def special(self):
        return ['box']

    def last_elements(self, lst, must_have=True):
        def iter():
            for k in lst:
                if k in self.dd or must_have:
                    yield self.dd[k][-1]

        return list(iter())

    def prepare_funcs(self, num):
        solver = Solver(self.data)

        for func in solver.iter_infinity(num):
            func.i = len(self.func_by_num)
            self.func_by_num.append(func)
            func.deps = sorted(frozenset(func.calc_deps()), key=lambda x: -x)
            self.dd[func.base].append(func.i)
            func.codec = 'pg'

    def find_first(self, name):
        return self.dd.get(name, [-1])[0]

    def register(self):
        for v in self.func_by_num:
            yield y.ELEM({'func': v.z})

        #if not self.dd['box']:
            #y.info('not data for ', self.info)

            #return

        #for v in [self.func_by_num[self.dd['box'][-1]]]:
            #yield y.ELEM({'func': v.z})

    def iter_deps(self):
        for f in self.func_by_num:
            for d in f.deps:
                yield f.i, d

    def exec_seq(self):
        return list(y.execution_sequence(self.iter_deps()))

    def out(self):
        for x in self.func_by_num:
            x.out_deps()

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


def make_proper_permutation(iface, info):
    yield y.EOP(y.ACCEPT('mf:original'), y.STATEFUL(), y.PROVIDES('mf:new functions'))

    data = []
    init_0(data)

    for row in iface.iter_data():
        print info, row

        if not row.data:
            break

        data.append(row)
        yield y.EOP()

    dt = Data(info, [x.data for x in data])
    dt.prepare_funcs(2)
    dt.out()

    for x in dt.register():
        yield x

    yield y.FIN()


async def async_make_proper_permutation(iface, info):
    yield y.EOP(y.ACCEPT('mf:original'), y.STATEFUL(), y.PROVIDES('mf:new functions'))

    data = []
    init_0(data)

    for row in iface.iter_data():
        if not row.data:
            break

        data.append(row)
        yield y.EOP()

    dt = Data(info, [x.data for x in data])
    dt.prepare_funcs(2)
    dt.out()

    for x in dt.register():
        yield x

    yield y.FIN()


def make_proper_permutation_gen(info):
    def func(iface):
        yield from make_proper_permutation(iface, info)

    func.__name__ = 'make_proper_permutation_' + y.small_repr(info)

    return func


def async_make_proper_permutation_gen(info):
    async def func(iface):
        async for x in async_make_proper_permutation(iface, info):
            yield x

    func.__name__ = 'async_make_proper_permutation_' + y.small_repr(info)

    return func


def init_0(where):
    @y.ygenerator(where=where)
    def box0():
        return {
            'meta': {
                'kind': ['special', 'tool'],
            },
        }
