from .ft import deep_copy
from .db import deref_pointer

MY_FUNCS = []


def split_name(b, c):
    return ('_'.join(['split', b.__name__] + [x.replace('/', '') for x in c])).replace('-', '_')


def x_key(v):
    a, b, c = v

    return split_name(b, c)


def real_calc(folders, func, info):
    fi = func(info)

    print 'real_calc', fi

    def iter_parts():
        yield func.__name__

        for x in folders:
            yield x[1:]

    bad_name = '_'.join(iter_parts())

    print bad_name

    return store_node({
        'node': {
            'build': [
                ('cp -R $(MNGR_%s_DIR)/%s $(INSTALL_DIR)/') % (bad_name.upper(), x[1:]) for x in folders
            ],
            'name': bad_name,
            'kind': 'splitter',
            'codec': 'xz',
            'func_name': func.__name__,
        },
        'deps': [],
    })


def splitter(folders=['/bin']):
    return helper
    return modifier(folders=folders, decorator='splitter')


def options(folders=['/bin']):
    return modifier(folders=folders, decorator='options')


def modifier(**kwargs):
    return lambda x: x
    res = deep_copy(kwargs)

    MY_FUNCS.append(res)

    def wrap_func(func):
        res['func'] = func

        def wrap_info(info):
            res['info'] = info

            return real_calc(res['folders'], res['func'], res['info'])()

        return wrap_info

    return wrap_func


def gen_func(args):
    if 'folders' in args:
        def func(info):
            return real_calc(args['folders'], args['func'], info)

        func.__name__ = args['func'].__name__

        return func


def gen_all_funcs():
    for args in MY_FUNCS:
        res = gen_func(args)

        if res:
            yield res
