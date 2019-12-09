def fix_user_data(iter):
    for f in iter:
        yield y.deep_copy(f)


def common_plugins(iface):
    yield y.EOP(y.ACCEPT(), y.PROVIDES('mf:plugin'))

    for el in sorted(y.file_data, key=lambda x: y.burn([3, x['name']])):
        if el['name'].startswith('pl/'):
            yield y.ELEM(y.deep_copy(el))

    yield y.FIN()


def mf_function_holder(iface):
    yield y.EOP(y.ACCEPT())
    
    lst = [
        y.common_plugins,
        y.my_funcs_cb,
        y.make_proper_permutation,
        y.exec_plugin_code,
    ]

    for l in lst:
        yield y.DEFUN(l)

    yield y.FIN()


def aggr_flag(name, metas):
    data = sum((m.get(name, []) for m in metas), [])

    try:
        return sorted(frozenset(data))
    except TypeError:
        return data
        
    
def join_metas(metas, merge=['flags']):
    return dict((x, aggr_flag(x, metas)) for x in merge) 


def apply_meta(to, fr):
    to.update(join_metas([to, fr]))
