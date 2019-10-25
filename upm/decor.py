import sys
import imp
import importlib
import functools
import itertools

from upm_iface import y


MY_FUNCS = {}
CALLBACKS = {}


def register_func_callback(func):
    CALLBACKS[func.__name__] = func


def main_reg(func, **kwargs):
    MY_FUNCS[func.__name__] = func

    return func


register_func_callback(main_reg)


def gen_key(func, info):
    return [func.__name__, info]


@y.cached(key=gen_key)
def gen_func(func, info):
    return y.store_node(y.fix_v2(y.deep_copy(y.call_v2(func, info))))


def options(**kwargs):
    res = y.deep_copy(kwargs)

    def functor(func):
        @functools.wraps(func)
        def wrapper(info):
            return gen_func(func, info)

        for cb in CALLBACKS.values():
            wrapper = cb(wrapper, **res)

        return wrapper

    return functor


def gen_all_funcs():
    for k in sorted(MY_FUNCS.keys()):
        yield MY_FUNCS[k]
