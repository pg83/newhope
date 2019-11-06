import sys
import imp
import importlib
import functools
import itertools


def gen_key(func, *args):
    return [func.__name__, args]


@y.cached(key=gen_key)
def gen_func(func, info, res):
    def my_fix_v2(arg):
        return y.fix_v2(arg, **res)

    return y.store_node(my_fix_v2(y.call_v2(func, info)))


def options(**kwargs):
    res = y.deep_copy(kwargs)

    def functor(func):
        @functools.wraps(func)
        def wrapper(info):
            return gen_func(func, info, res)

        assert wrapper

        for cb in y.callbacks().values():
            wrapper = cb(wrapper, **res)
            assert wrapper

        return wrapper

    return functor


def gen_all_funcs():
    mf = y.my_funcs()

    for k in sorted(mf.keys()):
        yield mf[k]
