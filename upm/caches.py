import atexit
import random
import functools
import itertools


def default_key(*args, **kwargs):
    return y.struct_dump_bytes([args, kwargs])


def restore_name(f):
    return f.__module__ + '.' + f.__name__


@y.singleton
def common_cache():
    return dict()


def get_copy_func(copy=False):
    if not copy:
        return lambda x: x

    def dc(x):
        try:
            return y.deep_copy(x)
        except ValueError:
            pass
        except TypeError:
            pass

        return x

    return dc


def cached(key=default_key, seed=None, copy=False):
    sdb = y.struct_dump_bytes
    k1 = sdb([key.__name__, seed or random.random()])

    def functor(f):
        k2 = sdb([f.__name__, k1])
        cc = common_cache()
        cf = get_copy_func(copy=copy)

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            k = sdb([key(*args, **kwargs), k2])

            if k not in cc:
                cc[k] = f(*args, **kwargs)

            return cf(cc[k])

        return wrapper

    return functor


def compose_simple(*funcs):
    def wrapper(*args, **kwargs):
        it = itertools.chain(list(funcs))

        for f in it:
            data = f(*args, **kwargs)

            for g in it:
                data = g(data)

            return data

    return wrapper


def compose_lisp(funcs):
    def wrapper(*args, **kwargs):
        f, ff = funcs
        data = f(*args, **kwargs)

        while ff:
            f, ff = ff
            data = f(data)

        return data

    return wrapper
