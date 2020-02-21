def common_plugins(cc):
    fd = y.globals.file_data

    for el in sorted(fd, key=lambda x: y.burn(x)):
        if el['name'].startswith('pl/'):
            el = y.dc(el)
            el['name'] = cc['os'] + '/' + cc['arch'] + '/' + el['name']

            yield {'el': el, 'cc': cc}


def generate_data(cc, cb, flat):
    tow = y.Tower(cc, flat)

    for el in common_plugins(cc):
        for func in y.exec_plugin_code(el):
            tow.on_data(func)

    for x in tow.gen_funcs():
        cb(x['func'])


def aggr_flag(name, metas):
    data = sum((m.get(name, []) for m in metas), [])

    try:
        return y.uniq_list_x(data)
    except TypeError:
        return data


def join_metas(metas, merge=['flags']):
    return dict((x, aggr_flag(x, metas)) for x in merge)


def gen_mk_data(cc, flat):
    funcs = []

    for c in cc:
        generate_data(c, funcs.append, flat)

    return funcs


def main_makefile(iter_cc, flat, kind='text'):
    cc = list(iter_cc())
    portion = gen_mk_data(cc, flat)

    def iter_data():
        for x in portion:
            yield x['code']()

    data = list(iter_data())

    return y.build_makefile(data, kind=kind)


def gen_package_name(x):
    res = x['gen']

    if res:
        res += '-'

    res += x['base']

    if 'num' in x:
        res += str(x['num'])

    return res


def fix_pkg_name(res, descr):
    res = y.dc(res)

    res['node']['name'] = gen_package_name(descr)
    res['node']['gen'] = descr['gen']

    return res

