@y.defer_constructor
@y.singleton
def my_funcs():
    all = []
    ids = {}

    @y.lookup
    def lookup(name):
        return ids[name]['code']
    
    @y.read_callback('new functions', 'collection')
    def cb(data):
        data = data['func']

        rec = {
            'data': data,
            'n': len(all),
        }

        rec['text_id'] = '_'.join((data['gen'], data['base'], str(rec['n'])))
        ids[rec['text_id']] = rec
        all.append(rec)

    return all


def gen_all_funcs():
    return [d['data']['code'] for d in my_funcs()]


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
