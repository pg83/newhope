@y.lookup
def lookup(name):
    return {'gen_func': y.signleton(lambda: y.compose_simple(y.call_v2, y.fix_v2, y.store_node))}[name]()
