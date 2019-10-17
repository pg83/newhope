import sys
import json
import marshal
import pstats
import hashlib
import functools
import cProfile


def dumps(s, **kwargs):
    return marshal.dumps(s, 4)
    #return json.dumps(s, **kwargs)


def loads(s):
    return marshal.loads(s)
    #return json.loads(s)


def deep_copy(x):
    return loads(dumps(x))


def struct_dump_bytes(p):
    return hashlib.md5(dumps(p, sort_keys=True)).digest()


def singleton(f):
    @functools.wraps(f)
    def wrapper():
        try:
            f.__res
        except AttributeError:
            f.__res = f()

        return f.__res

    return wrapper


def cached(f):
    vvv = {}

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        k = struct_dump_bytes([args, kwargs])

        if k not in vvv:
            vvv[k] = f(*args, **kwargs)

        return vvv[k]

    return wrapper


def fp(f, v, *args, **kwargs):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        return f(v, *args, **kwargs)

    return wrap


def profile(func, really=True):
    if not really:
        return func

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        p = cProfile.Profile()

        try:
            return p.runcall(func, *args, **kwargs)
        finally:
            ps = pstats.Stats(p, stream=sys.stderr)

            ps.sort_stats('cumtime')
            ps.print_stats()

    return wrapper
