@y.defer_constructor
@y.singleton
def my_funcs():
    res = {}

    @y.lookup
    def lookup(name):
        return res[name]['func']

    @y.read_callback('new functions', 'collection')
    def cb(data):
        func = data['func']
        res[func.__name__] = data

    return res


def gen_all_funcs():
    mf = my_funcs()

    for k in sorted(mf.keys()):
        yield mf[k]['func']
