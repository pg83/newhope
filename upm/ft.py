import json
import hashlib
import functools


def deep_copy(x):
    return json.loads(json.dumps(x))


def struct_dump(p):
    return hashlib.md5(json.dumps(p, sort_keys=True)).hexdigest()


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
        k = struct_dump([args, kwargs])

        if k not in vvv:
            vvv[k] = f(*args, **kwargs)

        return deep_copy(vvv[k])

    return wrapper


def fp(f, v, *args, **kwargs):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        return f(v, *args, **kwargs)

    return wrap
