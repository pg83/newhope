@y.singleton
def iter_all_tools():
    ff = y.fix_v2

    return [ff(x) for x in y.iter_system_tools()]


def iter_all_cc():
    return [y.dc(t) for t in y.iter_all_targets()]


def iter_tcs(os):
    if os:
        def iter_cc():
            for t in iter_all_cc():
                if t['os'] == os:
                    yield y.dc(t)
    else:
        iter_cc = iter_all_cc

    return iter_cc


@y.singleton
def group_by_cc():
    res = {}

    for x in iter_all_tools():
        assert x
        assert 'codec' in x['node']

        k = y.small_repr(x['node']['host'])

        if k in res:
            res[k].append(x)
        else:
            res[k] = [x]

        res['cc:' + k] = x['node']['host']

    return res


def find_toolchain_by_cc(cc):
    return y.dc(group_by_cc()[y.small_repr(cc)])


@y.singleton
def get_all_tc():
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
            'host': info,
            'meta': join_tc_meta(nodes),
        },
        'deps': [y.store_node(x) for x in tcs],
    }

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


def iterate_best_compilers(info):
    return score_toolchains(find_toolchain_by_cc(info), info)


def find_compiler_x(info):
    def do():
        for x in iterate_best_compilers(info):
            x = y.dc(x)
            x['node']['host'] = info

            yield y.store_node(x)

    return list(do())[:10]


@y.cached
def find_compiler_id(info):
    for x in find_compiler_x(info):
        return x

    raise Exception('shit happen %s' % info)
