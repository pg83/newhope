def gen_key(func, *args):
    return [func.__module__, func.__name__, args]


@y.cached(key=gen_key)
def gen_func(func, info):
    try:
        gen_func.__c
    except AttributeError:
        gen_func.__c = y.compose_simple(y.call_v2, y.fix_v2, y.store_node)
    
    return gen_func.__c(func, info)
