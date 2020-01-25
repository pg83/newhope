class FuncAggr(object):
    def __init__(self, cb):
        self.cb = cb
        self.v = []

    def on_new_data(self, iface):
        yield y.EOP(y.ACCEPT('mf:new functions', 'mf:splitted'))

        for row in iface.iter_data():
            data = row.data

            if data:
                self.cb(data['func'])
            else:
                self.v.append(1)

                if len(self.v) == 2:
                    yield y.FIN()
    
            yield y.EOP()


def gen_package_name(x):
    res = x['gen'] + '-' + x['base']

    if 'num' in x:
        res += str(x['num'])

    return res


def fix_pkg_name(res, descr):
    res = y.dc(res)

    res['node']['name'] = gen_package_name(descr)
    res['node']['gen'] = descr['gen']

    return res
