def common_plugins(cc, iface):
    yield y.EOP(y.ACCEPT(), y.PROVIDES('mf:plugin'))

    fd = y.globals.file_data

    for el in sorted(fd, key=lambda x: y.burn(x)):
        if el['name'].startswith('pl/'):
            el = y.dc(el)
            el['name'] = cc['os'] + '/' + cc['arch'] + '/' + el['name']

            yield y.ELEM({'el': el, 'cc': cc})

    yield y.FIN()


def common_plugins_gen(cc):
    def cc_plugins(iface):
        yield from common_plugins(cc, iface)

    return y.make_name(cc_plugins, 'cc_plugin_' + y.small_repr(cc))


def mk_funcs(cc, cb, iface):
    yield y.EOP(y.ACCEPT())

    lst_f = [
        common_plugins_gen(cc),
        y.exec_plugin_code,
        y.gen_towers,
        y.FuncAggr(cb).on_new_data,
    ]

    for l in lst_f:
        yield y.DEFUN(l)

    yield y.FIN()


def mk_funcs_gen(cc, cb):
    def func(iface):
        yield from mk_funcs(cc, cb, iface)

    return y.set_name(func, 'mk_funcs_' + y.small_repr(cc))


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
