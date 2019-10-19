from .ft import deep_copy


def split_name(b, c):
    return ('_'.join(['split', b.__name__] + [x.replace('/', '') for x in c])).replace('-', '_')


def x_key(v):
    a, b, c = v

    return split_name(b, c)


def real_calc(folders, func, info):
    fi = func(info)

    def iter_parts():
        yield func.__name__

        for x in folders:
            yield x[1:]

    bad_name = '_'.join(iter_parts())

    return store_node({
        'node': {
            'build': [
                ('cp -R $(MNGR_%s_DIR)/%s $(INSTALL_DIR)/') % (bad_name.upper(), x[1:]) for x in folders
            ],
            'name': bad_name,
            'kind': 'splitter',
            'codec': 'xz',
        },
        'deps': [fi, tar1(info), xz1(info), bestbox1(info)],
    })


def splitter(folders=['/bin']):
    return modifier(folders=folders)


def options(folders=['/bin']):
    return modifier(folders=folders)


def modifier(**kwargs):
    res = deep_copy(kwargs)

    def wrap_func(func):
        res['func'] = func

        def wrap_info(info):
            res['info'] = info

            return real_calc(**res)

        return wrap_info

    return wrap_func
