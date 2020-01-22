def gen_func(func):
    d = gen_func.__dict__

    try:
        d['']
    except KeyError:
        d[''] = y.compose_simple(y.call_v2, y.fix_v2, y.store_node)
    
    return d[''](func)
