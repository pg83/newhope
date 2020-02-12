@y.singleton
def get_decor():
    return y.compose_simple(y.call_v2, y.fix_v2, y.store_node)


def gen_func(func):
    return get_decor()(func)
