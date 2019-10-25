def split_part(kind, folders, func, info, my_func_name):
    func_name = func.__name__.upper()

    by_kind = {
        'dev': [
            'export CFLAGS="-I$(MNGR_%s_INC_DIR) $CFLAGS"' % func_name,
            'export LDFLAGS="-L$(MNGR_%s_LIB_DIR) $LDFLAGS"' % func_name,
        ],
        'run': [
            '$(ADD_PATH)',
            ],
        'doc': [],
        'log': [],
    }

    def iter_ops():
        if kind == 'run':
            yield 'mkdir -p $(INSTALL_DIR)/bin'

            for x in [('cp -R $(MNGR_%s_DIR)/%s/* $(INSTALL_DIR)/bin/ >& /dev/null') % (func_name, x[1:]) for x in folders]:
                yield x
        else:
            for y in (('cp -R $(MNGR_%s_DIR)/%s $(INSTALL_DIR)/') % (func_name, x[1:]) for x in folders):
                yield y

    #print my_func_name, func, y.restore_node(func(info))

    return to_v2({
        'code': '\n'.join(iter_ops()),
        'kind': 'split_part',
        'prepare': '\n'.join(by_kind[kind]),
        'deps': [func(info)], # + [y.xz2_run(info), y.tar2_run(info)],
        'name': my_func_name,
        'codec': 'xz',
    }, info)


REPACK_FUNCS = {
    'dev': ['/lib', '/include'],
    'run': ['/bin', '/sbin'],
    'doc': ['/share'],
    'log': ['/log'],
}


def splitter(func, **kwargs):
    repack = kwargs.get('repacks', REPACK_FUNCS)

    if repack:
        template = """
@y.options(repacks=None)
def {name}_{kind}(info):
    return split_part("{kind}", {folders}, y.{name}, info, "{name}_{kind}")

"""
        fn = func.__name__

        def iter_templates():
            for kind, folders in repack.items():
                    yield template.format(folders=str(folders), name=fn, kind=kind)

        for t in iter_templates():
            exec t in globals()

    return func


y.register_func_callback(splitter)
