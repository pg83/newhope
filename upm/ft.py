import sys
import json
import marshal
import pstats
import hashlib
import functools
import cProfile
import random


from upm_iface import y


def wraps(set_name='', use_cache=False, key_func=None, store_out=False, log_error=False):
    res = dict(set_name=set_name, use_cache=use_cache, key_func=key_func, store_out=store_out)

    def decorator(f):
        def logged_wrapper(func):
            @wraps(set_name='logged_' + func.__name__)
            def wrapper(arg):
                try:
                    return func(arg)
                except Exception as e:
                    y.xprint(str(f), str(arg), str(e), color='yellow')

                    raise e

            return wrapper

        def wrapper(arg):
            arg = f(arg)

            if store_out:
                arg = y.store_node(arg)

            return arg

        if log_error:
            wrapper = logged_wrapper(wrapper)

        scn = wraps(set_name='cached_' + wrapper.__name__)

        if use_cache:
            wrapper = scn(y.cached()(wrapper))
        elif key_func:
            wrapper = scn(y.cached(key=key_func)(wrapper))

        if set_name:
            try:
                wrapper.__name__ = set_name.__name__
            except AttributeError:
                wrapper.__name__ = set_name

        return wrapper

    return decorator


def singleton(f):
    @functools.wraps(f)
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
    restore = compose_simple(y.intern_struct, y.deref_pointer)

    def real_cached(f):
        rn_f = restore_name(f)

        @wraps(set_name='cached_' + f.__name__)
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
    @wraps(set_name=f)
    def wrap(*args, **kwargs):
        return f(v, *args, **kwargs)

    return wrap


def profile(func, really=True):
    if not really:
        return func

    @wraps(set_name=func)
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

    wrapper.__name__ = 'compose_' + '.'.join(f.__name__ for f in funcs)

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

