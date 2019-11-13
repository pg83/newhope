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


tmpl = """
def {holder}({vars}):
    def {name}(*args, **kwargs):
        k = sdb([key(*args, **kwargs), k2])

        if k not in cc:
            stats['m'] +=1
            cc[k] = f(*args, **kwargs) 
        else:
            stats['h'] += 1

        return cf(cc[k])

    return {name}
"""

def cached(key=default_key, seed=None, copy=False, enable_stats=False):
    sdb = y.struct_dump_bytes
    k1 = sdb([key.__name__, seed or y.random.random()])

    def functor(f):
        k2 = sdb([f.__name__, k1])
        cc = common_cache()
        cf = get_copy_func(copy=copy)
        hold_name = f.__name__.replace('.', '_')
        new_name = f.__name__.upper()

        stats = {'h': 0, 'm': 0}

        if enable_stats:
            def at_exit():
                print f.__module__ + '.' + f.__name__, stats

            y.atexit.register(at_exit)
            
        closure = {
            'sdb': sdb,
            'key': key,
            'k2': k2,
            'cc': cc,
            'f': f,
            'cf': cf,
            'stats': stats,
        }

        tm = tmpl.format(name=new_name, vars=', '.join(closure.keys()), holder=hold_name)
        m = __yexec__(tm, module_name=f.__module__ + '.ca')
        res = m[hold_name](**closure)

        y.prompt('/test2')

        return res

    return functor


def compose_simple(*funcs):
    def wrapper(*args, **kwargs):
        it = y.itertools.chain(list(funcs))

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
