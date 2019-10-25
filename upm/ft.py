import os
import sys
import json
import marshal
import pstats
import hashlib
import functools
import cProfile
import random


from upm_iface import y


def logged_wrapper(func):
    def wrapper(arg):
        try:
            return func(arg)
        except Exception as e:
            y.xprint(str(wrapper), str(f), str(arg), str(e), color='yellow')

            raise

    return wrapper


def copy_attrs(to, fr):
    #to.__module__ = fr.__module__
    to.__name__ = fr.__name__
    #to.__func__ = fr

    return to


class W(object):
    def __init__(self, w, args):
        self._w = w
        self._a = args

    def __call__(self, *args, **kwargs):
        return self._w(*args, **kwargs)

    def __str__(self):
        return '<functor {module}.{name} from {path}>'.format(**self._a)


def wrap_kw(func):
    def wrapper(*args, **kwargs):
        return func([args, kwargs])

    return copy_attrs(wrapper, func)


def unwrap_kw(func):
    def wrapper(arg):
        return func(*arg[0], **arg[1])

    return copy_attrs(wrapper, func)


def wraps(set_name=None, use_cache=False, key_func=None, store_out=False, log_error=False, log_time=False):
    def decorator(f):
        func = set_name or f
        path = os.path.basename(sys.modules[f.__module__].__file__)
        orig_f = f
        f = unwrap_kw(f)

        def wrapper(arg):
            arg = f(arg)

            if store_out:
                arg = y.store_node(arg)

            return arg

        if log_error:
            wrapper = logged_wrapper(wrapper)

        if use_cache:
            wrapper = y.cached()(wrapper)
        elif key_func:
            wrapper = y.cached(key=key_func)(wrapper)

        e = {}

        e['name'] = func.__name__
        e['module'] = func.__module__
        e['path'] = path

        wrapper = W(wrap_kw(wrapper), e)
        wrapper = copy_attrs(wrapper, orig_f)

        return wrapper

    return decorator


def singleton(f):
    def wrapper():
        try:
            f.__res
        except AttributeError:
            f.__res = f()

        return f.__res

    return wrapper


def default_key(*args, **kwargs):
    return y.struct_dump_bytes([args, kwargs])


def restore_name(f):
    return f.__module__ + '.' + f.__name__


def cached(key=default_key, seed=None):
    seed = seed or int((random.random() * 10000000))
    rn_key = restore_name(key)
    restore = compose_simple(y.intern_struct, y.load_struct)

    def real_cached(f):
        rn_f = restore_name(f)

        def slave(*args, **kwargs):
            x = {
                'k': rn_key,
                'f': rn_f,
                'v': key(*args, **kwargs),
                's': seed,
            }

            k = y.struct_dump_bytes(x)
            s = restore([k, {}])[1]

            if 'f' not in s:
                s['f'] = f(*args, **kwargs)

            return s['f']

        return slave

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


def compose_simple(*funcs):
    def wrapper(data):
        for f in funcs:
            data = f(data)

        return data

    return wrapper


def compose(*funcs, **kwargs):
    def num_args(f):
        try:
            f({}, [])
        except TypeError:
            return 1
        except Exception:
            return 2

        return 0

    def builder():
        for f in funcs:
            args = num_args(f)

            if args == 1:
                pass
            elif args == 2:
                ex = singleton(kwargs[f.__name__ + '_extra'])
                f = lambda x: f(x, ex())
            else:
                raise Exception('shit happen')

            yield f

    return compose_simple(*list(builder()))


def compose_rev(*funcs, **kwargs):
    return compose(*reversed(list(funcs)), **kwargs)

