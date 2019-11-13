@y.defer_constructor
@y.singleton
def my_funcs():
    all = []
    res = {}

    @y.lookup
    def lookup(name):
        return res[name]['func']

    @y.read_callback('new functions', 'collection')
    def cb(data):
        func = data['func']
        all.append(func)
        res[func.__name__] = data

    return all


def gen_all_funcs():
    return my_funcs()
