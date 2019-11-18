@y.lookup
def lookup(name):
    return {'gen_func': lambda: y.compose_simple(y.call_v2, y.fix_v2, y.store_node)}[name]()
