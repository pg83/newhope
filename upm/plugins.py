import sys
import os
import functools
import hashlib


def dep_name(dep):
    return y.restore_node(dep)['node']()['name']


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


def get_curl(n):
    return find_build_func(curl, n)

    assert n >= 3


def ygenerator(tier=None, kind=['user'], include=[], exclude=[], cached=[], version=1):
    def functor(func):
        assert tier is not None

        rfn = func.__name__
        fn = rfn[:-1]
        func.__name__ = rfn

        template = """
@y.options({options})
def {name}{num}(info):
    def my_tov2(x):
        return y.to_v2(x, info)

    kw = [
         ('info', info),
         ('deps', {deps}),
         ('num', {num}),
         ('func_name', '{func_name}'),
         ('codec', '{codec}'),
    ]

    return {tov2}(set_name({func_name}(**dict(kw)), "{name}{num}"))
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
            if len(cached) == 1:
                def key(**kwargs):
                    return kwargs[cached[0]]

                @y.cached(key=key)
                @functools.wraps(func)
                def wrapper(**kwargs):
                    return func(key(**kwargs))

                return wrapper

            def key(**kwargs):
                return dict((k, kwargs[k]) for k in cached)

            @y.cached(key=key)
            @functools.wraps(func)
            def wrapper(**kwargs):
                return func(**key(**kwargs))

            return wrapper

        return func

    return functor
