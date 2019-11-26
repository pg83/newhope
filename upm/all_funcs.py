@y.defer_constructor
@y.singleton
def my_funcs():
    all = []
    ids = {}
    v = []
    
    @y.lookup
    def lookup(name):
        return ids[name]['code']

    return all, ids, v


def my_funcs_cb(iface):
    all, ids, v = my_funcs()
    
    yield y.EOP(y.ACCEPT('mf:new functions', 'mf:splitted'))

    for row in iface.iter_data():
        data = row.data

        if not data:
            v.append(1)
            
            if len(v) == 2:
                yield y.FIN()
                
            yield y.EOP()

            return
            
        data = data['func']

        rec = {
            'data': data,
            'n': len(all),
        }
            
        rec['text_id'] = '_'.join((data['gen'], data['base'], str(rec['n'])))
    
        ids[rec['text_id']] = rec
        all.append(rec)

    yield y.EOP()

        
def gen_all_funcs():
    return [d['data']['code'] for d in my_funcs()[0]]


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
