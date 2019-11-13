@y.defer_constructor
def init():
    @y.read_callback('build env', 'towers')
    def solver(arg):
        arg['back_channel']({'func': lambda info: {}, 'descr': ['system', 'fast']})


def make_proper_permutation(data):
    v = set()

    def flt():
        for z in data:
            func = z.pop('func')
            x = y.deep_copy(z)
            z['func'] = func
            x['func'] = func
            
            if 'name' not in x:
                x['name'] = x['func'].__name__[:-1]

            assert x['name'] not in v

            v.add(x['name'])
            x['name'] = 'tow_' + x['name']

            yield x

    data = list(flt())
    by_name = dict((x['name'], x) for x in data)

    subst = {
        'intl': 'gettext',
        'iconv': 'libiconv',
    }
                       
    def dep_list(x):
        r = x['func']()

        if x['name'] == 'tow_make':
            extra = []
        else:
            extra = ['tow_make']

        return extra + ['tow_' + subst.get(x, x) for x in r.get('meta', {}).get('depends', [])]

    def iter_items():
        r, w = y.make_engine(data, dep_list=dep_list)
            
        for el in r():
            w(el['i'])
            yield el['x']
                
    def iter_infinity():
        while True:
            for i in iter_items():
                yield i
        
    @y.cached()
    def full_deps(n):
        my_deps = dep_list(by_name[n])

        if not my_deps:
            return []

        def iter_lst():
            yield my_deps

            for y in my_deps:
                yield full_deps(y)

        return list(frozenset(sum(iter_lst(), [])))

    d = y.collections.defaultdict(list)
    func_by_num = {}

    @y.cached()
    def select_deps(name):
        def do():
            for k in full_deps(name):
                v = d[k]

                if not v:
                    continue
                elif len(v) == 1:
                    yield v[0]
                elif len(v) == 2:
                    yield v[1]
                else:
                    yield y.random.choice(v)

        return list(do())

    for i, x in enumerate(iter_infinity()):
        name = {'i': i, 'x': x}
        name['d'] = select_deps(name['x']['name'])
        d[x['name']].append(i)
        func_by_num[i] = name

        if i > 100:
            break

    res = {}

    @y.cached()
    def run_func(info, i):
        v = func_by_num[i]

        data = y.deep_copy(v['x']['func']())
        data['deps'] = [res[j](info) for j in v['d']]
        data['name'] = res[i].__base_name__
        
        n = y.to_v2(data, info)
        n['node']['num'] = i

        return n

    def gen_f(i, v):
        name = v['x']['name']

        f1 = lambda info: run_func(info, i)
        f1.__name__ = 'f1_' + name + '_' + str(i)
        f2 = lambda info: y.gen_func(f1, info, {})
        f2.__name__ = 'f2_' + name + '_' + str(i)
        f3 = y.cached()(f2)
        f3.__name__ = v['x']['name'] + str(i)
        f3.__base_name__ = v['x']['name']

        return f3

    for i, v in func_by_num.items():
        res[i] = gen_f(i, v)

    wc = y.write_channel('new functions', 'towers')

    for i, f in res.items():
        wc({'func': f, 'rfunc': func_by_num[i]['x']['func'].__name__, 'kind': ['tower']})


def make_perm():
    make_proper_permutation(y.original_funcs())
