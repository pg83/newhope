@y.singleton
def iter_all_tools():
    ff = y.fix_v2

    def do():
        for x in y.iter_system_tools():
            yield ff(x)

    return list(do())


@y.singleton
def group_by_cc():
    res = {}

    for x in iter_all_tools():
        assert x
        assert 'codec' in x['node']

        k = y.small_repr_cons(x['node']['constraint'])

        if k in res:
            res[k].append(x)
        else:
            res[k] = [x]

        res['cc:' + k] = x['node']['constraint']

    return res


def find_toolchain_by_cc(cc):
    return y.deep_copy(group_by_cc()[y.small_repr_cons(cc)])


@y.singleton
def get_all_constraints():
    res = []
    cc = group_by_cc()

    for k in sorted(cc.keys()):
        if k.startswith('cc:'):
            res.append(cc[k])

    return res


def score_tc(c, l, cpp):
    s = 0

    for t in (c, l, cpp):
        st = str(t)

        if 'clang' in st:
            s += 10
            
        if 'clang++' in st:
            s += 20

        if 'lld' in st:
            s += 100

    return s


def join_tc_meta(tcs):
    return {
        'kind': y.uniq_list_3(sum((x['meta']['kind'] for x in tcs), [])),
        'provides': sum((x['meta']['provides'] for x in tcs), []),
    }

    
def join_toolchains(info, tcs):
    nodes = [x['node'] for x in tcs]
    res = {
        'node': {
            'build': [],
            'prepare': sum((x.get('prepare', []) for x in nodes), []),
            'name': 'tc-' + '-'.join(x['name'] for x in nodes),
            'version': y.burn(nodes),
            'constraint': info,
            'meta': join_tc_meta(nodes),
        },
        'deps': [y.store_node(x) for x in tcs],
    }

    print res
    
    return y.fix_v2(res)


def score_toolchains(lst, info):
    def flt(kind):
        for o in lst:
            if kind in o['node']['meta']['kind']:
                yield o

    cc = list(flt('c'))
    cxx = list(flt('c++'))
    link = list(flt('linker'))

    def gen_all():
        for c in cc:
            for cpp in cxx:
                for l in link:
                    yield {'c': c, 'l': l, 'c++': cpp, 's': score_tc(c, l, cpp)}

    toolchains = list(sorted(list(gen_all()), key=lambda x: -x['s']))

    return [join_toolchains(info, [x['c'], x['c++'], x['l']]) for x in toolchains]


@y.cached()
def iterate_best_compilers(info):
    return score_toolchains(find_toolchain_by_cc(info), info)


def find_compiler_x(info):
    def do():
        for x in iterate_best_compilers(info):
            x = y.deep_copy(x)
            x['node']['constraint'] = info

            yield y.store_node(x)

    return list(do())[:10]


def join_versions(deps):
    def iter_v():
        for d in deps:
            yield y.restore_node_node(d)['version']

    return '-'.join(iter_v())


@y.cached()
def find_compiler_id(info):
    for x in find_compiler_x(info):
        return x

    raise Exception('shit happen %s' % info)


@y.cached()
def find_compilers(info):
    def iter_compilers():
        if y.is_cross(info):
            host = info['host']

            yield find_compiler_id({'target': host, 'host': host})

        yield find_compiler_id(info)

    return list(iter_compilers())
