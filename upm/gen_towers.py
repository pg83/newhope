import sys

ic = y.inc_counter()


@y.singleton
def is_debug():
    return 'debug' in y.config.get('tow', '')


class Func(object):
    def __init__(self, x, data):
        self.x = x
        self.inc_count = ic()
        self.data = data
        self.i = 0

    def out_deps(self):
        y.xprint_db('{dr}' + str(self) + '{}', '->', '(' + ', '.join([str(self.data.func_by_num[i]) for i in self.deps]) + ')')

    def contains(self):
        return self.code().get('meta', {}).get('contains', [])

    def __str__(self):
        return '<' + self.base  + '-' + str(self.i) + '-' + self.compact_kind() + '>'

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
        return self.x['kind']

    @property
    def code(self):
        return self.x['code']

    @property
    def base(self):
        return self.x['base']

    @y.cached_method
    def raw_depends(self):
        subst = {
            'intl': 'gettext',
            'iconv': 'libiconv',
            'c++': 'libcxx',
            'm4': 'quasar-m4',
        }
        
        return [subst.get(x, x) for x in self.code().get('meta', {}).get('depends', [])]
    
    def depends(self):
        return self.raw_depends()

    @y.cached_method
    def all_depends(self):
        return y.uniq_list_3(sum([self.data.by_name[x].all_depends() for x in self.depends()], [x for x in self.depends()]))
    
    @y.cached_method
    def dep_lib_list(self):
        def iter():
            for x in self.dep_list():
                if self.data.by_name[x].is_library:
                    yield x

        return list(iter())

    @y.cached_method
    def dep_tool_list(self):
        def iter():
            for x in self.dep_list():
                y = self.data.by_name[x]
                
                if y.is_tool or not y.is_library:
                    yield x
                    
        return list(iter())

    @y.cached_method
    def dep_list(self):
        def iter1():            
            yield from self.depends()

            for d in ('make', 'musl', 'bestbox'):
                if self.base in self.data.find_func(d).all_depends():
                    continue
                
                if self.base == d:
                    continue

                if 'code' not in self.code():
                    continue
                
                yield d

        res = list(iter1())

        #print(self.base, res, file=sys.stderr)

        return res

    @y.cached_method
    def run_func(self, info):
        data = y.deep_copy(self.c(info))
        data['deps'] = y.uniq_list_3(data['deps'] + self.data.calc(self.deps, info))
        data['node']['codec'] = self.codec
        
        y.apply_meta(data['node']['meta'], y.join_metas([y.restore_node_node(d).get('meta', {}) for d in data['deps']]))
        
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
        return self.data.optimize(self.data.select_deps(self.base) + self.data.last_elements(self.data.special, must_have=False))


class SpecialFunc(Func):
    def __init__(self, x, data):
        Func.__init__(self, x, data)

    def depends(self):
        return self.data.by_kind[self.base]
    
    @y.cached_method
    def contains(self):
        def it():
            deps = self.depends()

            yield deps

            for x in deps:
                yield self.data.by_name[x].contains()
            
        res = y.uniq_list_3(sum([x for x in it()], []))
        
        return res
    
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
        self.inc_count = ic()
        self.data = [self.create_object(x['func']) for x in sorted(data, key=lambda x: x['func']['base'])]
        self.by_name = dict((x.base, x) for x in self.data)

    def create_object(self, x):
        if x['base'] in self.special:
            return SpecialFunc(x, self)

        return Func(x, self)

    def optimize(self, deps):
        contains = frozenset(sum([self.func_by_num[i].contains() for i in deps], []))

        def iter_deps():
            for d in deps:
                f = self.func_by_num[d]
                
                if f.is_library:
                    yield d
                elif f.base in contains:
                    pass
                else:
                    yield d

        return list(iter_deps())
    
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
            func.deps = sorted(func.calc_deps())                
            self.dd[func.base].append(func.i)

            if frozenset(func.deps).isdisjoint(frozenset(self.dd.get('compression', []))):
                func.codec = 'pg'
            else:
                func.codec = '7z'
                
            if all((len(self.dd.get(x, [])) >= num) for x in self.special):
                break

    def find_first(self, name):
        return self.dd.get(name, [-1])[0]
            
    def register(self):
        for v in self.func_by_num:
            yield y.ELEM({'func': v.z})
        
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

    def find_func(self, name):
        return self.by_name[name]
    
    def select_deps(self, name):
        return self.last_elements(self.full_deps(name))

    @y.cached_method
    def calc(self, deps, arg):
        return [self.func_by_num[d].f(arg) for d in deps]
    
    
def make_proper_permutation(iface):
    yield y.EOP(y.ACCEPT('mf:original'), y.STATEFUL(), y.PROVIDES('mf:new functions'))

    data = []
    init_0(data)
    
    for row in iface.iter_data():
        if not row.data:
            break
        
        data.append(row)
        yield y.EOP()

    dt = Data([x.data for x in data])
    dt.prepare_funcs(2)
    dt.out()
    
    for x in dt.register():
        yield x
        
    yield y.FIN()

    
def init_0(where):
    @y.ygenerator(where=where)
    def box0():
        return {
            'meta': {
                'depends': ['compression'],
                'kind': ['special', 'tool'],
            },
        }

    @y.ygenerator(where=where)
    def compression0():
        return {
            'meta': {
                'kind': ['special', 'tool', 'box'],
            },
        }
