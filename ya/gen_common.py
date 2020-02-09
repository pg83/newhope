def common_plugins(cc):
    fd = y.globals.file_data

    for el in sorted(fd, key=lambda x: y.burn(x)):
        if el['name'].startswith('pl/'):
            el = y.dc(el)
            print el, cc
            el['name'] = cc['os'] + '/' + cc['arch'] + '/' + el['name']

            yield {'el': el, 'cc': cc}


def generate_data(cc, cb, distr):
    tow = y.Tower(distr, cc)
    
    for el in common_plugins(cc):
        for func in y.exec_plugin_code(el):
            tow.on_data(func)
            
    for x in tow.gen_funcs():
        cb(x['func'])


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
