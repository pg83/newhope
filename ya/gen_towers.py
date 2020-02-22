ic = y.inc_counter()


@y.singleton
def get_decor():
    return y.compose_simple(y.call_v2, y.fix_v2, y.store_node)


def gen_func(func):
    return get_decor()(func)


@y.singleton
def is_debug():
    return 'debug' in y.config.get('tow', '')


@y.cached
def subst_by_platform(info):
    common = {
        'intl': 'gettext',
        'iconv': 'libiconv',
        'c++': 'libcxx',
        'm4': 'gnu-m4',
        'termcap': 'ncurses',
        'ncurses': 'ncurses-real',
        'pcre': 'pcre2',
        'c': 'sys_libc',
    }

    by_os = {
        'linux': common.copy(),
        'darwin': common.copy(),
    }

    by_os['linux'].update({'ncurses': 'netbsd-curses'})
    by_os['linux'].update({'libtool': 'slibtool'})
    by_os['linux'].update({'m4': 'quasar-m4'})
    by_os['linux'].update({'c': info.get('libc', 'musl')})

    res = y.dc(by_os[info['os']])

    for k in list(res.keys()):
        for s in y.repacks_keys():
            res[k + '-' + s] = res[k] + '-' + s

    return res


class Func(object):
    @y.cached_method
    def do_subst(self, x):
        sd = self.subst_dict

        x = sd.get(x, x)
        x = sd.get(x, x)

        return x

    def __init__(self, x, data):
        self.x = x
        self.inc_count = ic()
        self.data = data
        self.codec = 'pg'

    @property
    @y.cached_method
    def subst_dict(self):
        return subst_by_platform(self.data.info)

    def out_deps(self):
        y.info('{dr}' + str(self) + '{}', '->', '(' + ', '.join([str(self.data.func_by_num[i]) for i in self.deps]) + ')')

    def contains(self):
        return self.code().get('meta', {}).get('contains', [])

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

    def raw_depends(self):
        code = self.code()

        if code:
            for x in self.code().get('meta', {}).get('depends', []):
                yield self.do_subst(x)

    @y.cached_method
    def depends(self):
        return list(self.raw_depends())

    @y.cached_method
    def dep_lib_list(self):
        def iter():
            for x in self.depends():
                if self.data.by_name[self.g][x].is_library:
                    yield x

        return y.uniq_list_x(iter())

    @y.cached_method
    def dep_tool_list(self):
        def iter():
            for x in self.depends():
                if not self.data.by_name[self.g][x].is_library:
                    yield x

        return y.uniq_list_x(iter())

    @y.cached_method
    def run_func(self):
        data = y.dc(self.c())

        data['deps'] = y.uniq_list_x(data['deps'] + self.data.calc(self.deps))
        data['node']['codec'] = self.codec

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
            'info': self.data.info,
        }

    def clone(self):
        return Func(self.x, self.data)

    def busybox_boot(self):
        res = self.data.busybox_boot()

        if self.i in res:
            return []

        return res

    def calc_extra(self):
        if self.base == 'box':
            return []

        if self.data.flat:
            return self.busybox_boot()

        bg = self.data.box_by_gen.get(self.g - 1)

        if bg is None:
            return self.busybox_boot()

        return [bg.i]

    @y.cached_method
    def calc_deps(self):
        return self.data.optimize(self.data.select_deps(self.base, self.g) + self.calc_extra(), self)

    @property
    @y.cached_method
    def deps(self):
        return sorted(self.calc_deps(), key=lambda x: -x)


class SplitFunc(Func):
    def __init__(self, func, split):
        Func.__init__(self, func.x, func.data)
        self._func = func
        self._split = split

    @property
    def base(self):
        return self._func.base + '-' + self._split

    def clone(self):
        return SplitFunc(self._func, self._split)

    def code(self):
        return y.run_splitter(self._func, self._split)

    @y.cached_method
    def calc_deps(self):
        return self.data.last_elements([self._func.base]) + self.calc_extra()


class Solver(object):
    def __init__(self, data, generation=0, seed=1):
        self._generation = generation
        self._data = data
        self._by_base = dict((x.base, i) for i, x in enumerate(self._data))
        self._seed = seed

        def iter_deps():
            for i, x in enumerate(self._data):
                for y in x.depends():
                    yield i, self._by_base[y]

                yield i, None

        self._r, self._w = y.simple_engine(iter_deps(), seed=self._seed)
        self.inc_count = ic()

    def next_solver(self):
        return Solver(self._data, generation=(self._generation + 1), seed=(self._seed * 13 + 17))

    def iter_items(self):
        y.debug('run solver')

        for el in self._r():
            self._w(el)
            yield self._data[el]

        y.debug('done')


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
    def __init__(self, info, flat, data):
        self.flat = flat
        self.info = info
        self.new_funcs = []
        self.by_name = y.collections.defaultdict(dict)
        self.box_by_gen = {}
        self.dd = y.collections.defaultdict(list)
        self.func_by_num = []
        self.inc_count = ic()

        def iter_objects():
            for x in sorted(data, key=lambda x: x['base']):
                f = self.create_object(x)

                yield f

                for k in y.repacks_keys():
                    yield SplitFunc(f, k)

        self.data = list(iter_objects())
        self.prepare_funcs(3)

    def busybox_boot(self):
        return self.last_elements(['busybox-boot'], must_have=False)

    def create_object(self, x):
        return Func(x, self)

    def optimize(self, deps, what):
        def it():
            for i in deps:
                yield from self.func_by_num[i].contains()

        contains = frozenset(it())

        def iter_deps():
            for d in deps:
                f = self.func_by_num[d]

                if f.is_library and f.is_tool:
                    yield d
                elif f.base in contains:
                    if what.base.startswith(f.base):
                        yield d
                else:
                    yield d

        return y.uniq_list_x(iter_deps())

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
                self.calc_new_deps()
                pg = g

            if g >= num:
                break

            if g == num - 1:
                func.gen = ''
            else:
                func.gen = 'tow' + str(g)

            self.add_func(func, g)

    def calc_new_deps(self):
        for func in self.new_funcs:
            _ = func.deps

        self.new_funcs = []

    def add_func(self, func, g):
        if func.base == 'box':
            self.box_by_gen[g] = func

        func.g = g
        func.i = len(self.func_by_num)

        self.new_funcs.append(func)
        self.by_name[g][func.base] = func
        self.func_by_num.append(func)
        self.dd[func.base].append(func.i)

    def find_first(self, name):
        return self.dd.get(name, [-1])[0]

    def register(self):
        for i in self.last_elements(self.dd.keys()):
            v = self.func_by_num[i]

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

        y.info('{bg}exec sequence', str(self.exec_seq()[:100])[:-1] + ', ...', '{}')

    def full_deps(self, name, g):
        return y.uniq_list_x(self.full_lib_deps(name, g) + self.full_tool_deps(name, g))

    @y.cached_method
    def full_lib_deps(self, name, g):
        my_deps = self.by_name[g][name].dep_lib_list()

        def iter_lst():
            for y in my_deps:
                yield y
                yield from self.full_lib_deps(y, g)

        return y.uniq_list_x(iter_lst())

    @y.cached_method
    def full_tool_deps(self, name, g):
        return y.uniq_list_x(self.by_name[g][name].dep_tool_list())

    def select_deps(self, name, g):
        return self.last_elements(self.full_deps(name, g))

    @y.cached_method
    def calc(self, deps):
        return [self.func_by_num[d].f() for d in deps]


class Tower(object):
    def __init__(self, cc, flat):
        self._data = []
        self._cc = cc
        self._flat = flat

    def on_data(self, data):
        y.debug('will gen func for', data['base'])
        self._data.append(data)

    def gen_funcs(self):
        dt = Data(self._cc, self._flat, [x for x in self._data])
        #dt.out()

        cnt = 0

        for x in dt.register():
            cnt += 1
            yield x

        if not cnt:
            y.error('{br}no package detected in', self._cc, '{}')
