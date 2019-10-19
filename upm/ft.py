import sys
import json
import marshal
import pstats
import hashlib
import functools
import cProfile


def dumps(s, **kwargs):
    return json.dumps(s, sort_keys=True)


def loads(s):
    return json.loads(s)


def deep_copy(x):
    return loads(dumps(x))


def struct_dump_bytes(p):
    return hashlib.md5(dumps(p, sort_keys=True)).hexdigest()[:16]


def singleton(f):
    @functools.wraps(f)
    def wrapper():
        try:
            f.__res
        except AttributeError:
            f.__res = f()

        return f.__res

    return wrapper


def cached(key=lambda x: x):
    vvv = {}

    def real_cached(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            k = struct_dump_bytes(key({'a': args, 'b': kwargs, 'c': f.__name__}))

            if k not in vvv:
                vvv[k] = f(*args, **kwargs)

            return vvv[k]

        return wrapper

    return real_cached


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
