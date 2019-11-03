import sys
import os
import functools
import hashlib
import inspect


def dep_name(dep):
    return y.restore_node(dep)['node']['name']


def dep_list(info, iter):
    return [x(info) for x in iter]


def reg_func_cb(x):
    y.register_func_callback(x)


def exec_plugin_code(code):
    exec compile(code, __file__, 'exec') in globals()


def find_build_func(name, num='', split=''):
    if num:
        name = name + str(num)

    if split:
        name = name + '_' + split

    return globals()[name]


def identity(x):
    return x


def parse_line(l):
    if l.startswith('source fetch '):
        return l.split('"')[1]

    return False


def set_name(v, n):
    v = y.deep_copy(v)
    v['name'] = n

    return v


def ygenerator(tier=None, kind=['user'], include=[], exclude=[], cached=True, version=1):
    def functor(func):
        assert tier is not None

        rfn = func.__name__
        fn = rfn[:-1]
        func.__name__ = rfn

        template = """
@y.options({options})
def {name}{num}(info):
    kw = [
         ('info', info),
         ('deps', {deps}),
         ('num', {num}),
         ('func_name', '{func_name}'),
         ('codec', '{codec}'),
    ]

    kw = dict(kw)

    def my_tov2(x):
        if 'deps' not in x:
            x['deps'] = x.pop('extra_deps', []) + kw['deps']

        return y.to_v2(x, info)

    return {tov2}(set_name({func_name}(**kw), "{name}{num}"))
"""
        fname = 'identity'

        if version == 1:
            fname = 'my_tov2'

        data = {
            'tier': tier,
            'name': fn,
            'kind': kind,
            'include': include,
            'exclude': exclude,
            'template': template,
            'extra_arg': {
                'func_name': func.__name__,
                'tov2': fname,
            }
        }

        if fn.startswith('lib'):
            kind.append('library')

        y.register_func_generator(data)

        if cached:
            args = inspect.getargspec(func)[0]

            def key(**kwargs):
                return [kwargs[arg] for arg in args]

            @y.cached(key=key)
            @functools.wraps(func)
            def wrapper(**kwargs):
                return func(*key(**kwargs))

            return wrapper

        return func

    return functor
