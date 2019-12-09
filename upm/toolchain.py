@y.singleton
def iter_all_tools():
    ff = y.fix_v2

    def do():
        for x in y.itertools.chain(y.iter_system_tools(), y.iter_ndk_tools()):
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


def score_pair(c, l):
    return y.struct_dump_bytes([c, l])


def join_toolchains(c, l, info):
    cn = c['node']
    ln = l['node']

    return y.fix_v2({
        'node': {
            'build': [],
            'prepare': cn.get('prepare', []) + ln.get('prepare', []),
            'kind': cn['meta']['kind'] + ln['meta']['kind'],
            'name': cn['name'] + '-' + ln['name'],
            'version': cn['version'] + '-' + ln['version'],
            'constraint': info,
        },
        'deps': [y.store_node(c), y.store_node(l)]
    })


def score_toolchains(lst, info):
    def flt(kind):
        for o in lst:
            if kind in o['node']['meta']['kind']:
                yield o

    comp = list(flt('c'))
    link = list(flt('linker'))

    def gen_all():
        for c in comp:
            for l in link:
                yield {'c': c, 'l': l, 's': score_pair(c, l)}

    toolchains = list(sorted(list(gen_all()), key=lambda x: x['s']))

    return [join_toolchains(x['c'], x['l'], info) for x in toolchains]


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
