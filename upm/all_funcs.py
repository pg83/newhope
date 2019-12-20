@y.singleton
def my_funcs():
    data = {
        'all': [],
        'ids':  {},
        'v':  [],
    }
    
    @y.lookup
    def lookup(name):
        return data['ids'][name]['code']

    return data


def my_funcs_cb(iface, cb):
    yield y.EOP(y.ACCEPT('mf:new functions', 'mf:splitted'))

    data = my_funcs()
    all = data['all']
    ids = data['ids']
    v = data['v']

    for row in iface.iter_data():
        data = row.data

        if not data:
            v.append(1)
            
            if len(v) == 2:                
                yield y.FIN()
                
            yield y.EOP()

            return

        data = data['func']

        cb(data['code'])

        rec = {
            'data': data,
            'n': len(all),
        }

        rec['text_id'] = '_'.join((data['gen'], data['base'], str(rec['n'])))    
        ids[rec['text_id']] = rec
        all.append(rec)

    yield y.EOP()


def gen_package_name(x):
    res = x['gen'] + '-' + x['base']

    if 'num' in x:
        res += str(x['num'])

    return res


def fix_pkg_name(res, descr):
    res = y.deep_copy(res)

    res['node']['name'] = gen_package_name(descr)
    res['node']['gen'] = descr['gen']

    return res
