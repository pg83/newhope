def default_key(*args, **kwargs):
    return y.burn([args, kwargs])


def restore_name(f):
    return f.__module__ + '.' + f.__name__


@y.singleton
def common_cache():
    return dict()


def get_copy_func(copy=False):
    if not copy:
        return lambda x: x

    return lambda x: y.dc(x)


tmpl = """
def {holder}({vars}):
    sdb = y.burn
    cc = y.common_cache()
    stats = dict(h=0, m=0)
    uniq = (y.random.random() * 10000000000000)

    def at_exit():
        if y.config.get('cache_stats'):
            y.xprint_w('{{y}}' + f.__module__ + '.' + f.__name__, '{{w}}->', '{{b}}' + str(stats))

    y.run_at_exit(at_exit)

    def {name}(*args, **kwargs):
        k = sdb([key(*args, **kwargs), uniq])

        if k not in cc:
            stats['m'] +=1
            cc[k] = f(*args, **kwargs) 
        else:
            stats['h'] += 1

        return cf(cc[k])

    return {name}
"""


def simple_cache(f):
    c = {}

    def wrapper(*args):
        key = y.burn(args)

        try:
            return c[key]
        except KeyError:
            c[key] = f(*args)

        return c[key]

    return wrapper


@simple_cache
def get_cache_holder_module(template, name):
    return __yexec__(template, module_name='gn.cachers.' + name)


def get_cache_holder(f, ic=y.inc_counter()):
    if '<lambda>' in f.__name__:
        f.__name__ = '[' + y.inspect.getsource(f).strip() + ']'
        name = 'lambda_' + str(ic())
    else:
        name = f.__name__

    hold_name = 'cache_holder_' + name
    vars = ', '.join(['key', 'f', 'cf'])

    return get_cache_holder_module(tmpl.format(name=name.upper(), vars=vars, holder=hold_name), name)[hold_name]


def cached(f=None, key=default_key, copy=False):
    cf = get_copy_func(copy=copy)

    def functor(f):
        return get_cache_holder(f)(key, f, cf)

    if f:
        return functor(f)

    return functor


def compose_simple(*funcs):
    def wrapper(*args, **kwargs):
        it = y.itertools.chain(funcs)

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


def cached_method(meth):
    def wrapper(self, *args, **kwargs):
        try:
            self.__cache__
        except Exception:
            self.__cache__ = {}

        d = self.__cache__
        k = y.burn([args, kwargs, meth.__name__])[:8]

        if k not in d:
            d[k] = meth(self, *args, **kwargs)

        return d[k]

    return wrapper
