def fix_user_data(iter):
    for f in iter:
        f = y.deep_copy(f)
        ss = f.get('support', [])

        if ss and 'darwin' not in ss:
            continue

        yield f


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
