import itertools


@y.singleton
def iter_all_tools():
    ff = y.fix_v2

    def do():
        for x in itertools.chain(y.iter_system_tools(), y.iter_musl_cc_tools(), y.iter_ndk_tools()):
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

    return res


def find_toolchain_by_cc(cc):
    return group_by_cc()[y.small_repr_cons(cc)]


def find_compiler(info):
    for d in find_toolchain_by_cc(info):
        yield d


def join_versions(deps):
    def iter_v():
        for d in deps:
            yield y.restore_node(d)['node']()['version']

    return '-'.join(iter_v())


@y.cached()
def find_compiler_id(info):
    for x in find_compiler(info):
        return x

    raise Exception('shit happen %s' % info)


@y.cached()
def find_compilers(info):
    def iter_compilers():
        if y.is_cross(info):
            host = info['host']

            yield find_compiler_id({'target': host, 'host': host})

        yield find_compiler_id(info)

    return [y.store_node(x) for x in iter_compilers()]
