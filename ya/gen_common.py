def fix_user_data(iter):
    for f in iter:
        yield y.deep_copy(f)


def common_plugins(iface):
    yield y.EOP(y.ACCEPT(), y.PROVIDES('mf:plugin'))

    for el in sorted(y.globals.file_data, key=lambda x: y.burn([3, x['name']])):
        if el['name'].startswith('pl/'):
            yield y.ELEM(y.deep_copy(el))

    yield y.FIN()


def mf_function_holder(cc, cb, iface):
    yield y.EOP(y.ACCEPT())
    
    lst_f = [
        y.common_plugins,
        y.FuncAggr(cb).on_new_data,
        y.exec_plugin_code,
    ] + [y.make_proper_permutation_gen(x) for x in cc]

    for l in lst_f:
        yield y.DEFUN(l)

    lst_c = [
    ]

    for l in lst_c:
        yield y.DECORO(l)
    
    yield y.FIN()

    
def mf_function_holder_gen(cc, cb):
    def func(iface):
        yield from mf_function_holder(cc, cb, iface)

    func.__name__ = 'mf_function_holder_generator_' + '_'.join(str(x) for x in cc)

    return func


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
