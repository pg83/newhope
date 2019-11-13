def gen_key(func, *args):
    return [func.__name__, args]


@y.cached(key=gen_key)
def gen_func(func, info, res):
    def my_fix_v2(arg):
        return y.fix_v2(arg, **res)

    c = y.compose_simple(y.call_v2, my_fix_v2, y.store_node)

    return c(func, info)


def options(**kwargs):
    res = y.deep_copy(kwargs)
    channel = res.pop('channel', None)
    
    if channel:
        channel = eval(channel)

    def functor(func):
        @y.functools.wraps(func)
        def wrapper(info):
            return gen_func(func, info, res)

        if channel:
            channel({'func': wrapper, 'rfunc': str(func), 'kind': ['options']})

        return wrapper

    return functor
