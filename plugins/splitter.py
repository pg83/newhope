def split_part(kind, folders, func, info):
    try:
        func_name = func.__base_name__.upper()
    except:
        func_name = func.__name__.upper()

    my_name = (func_name + '_' + kind).upper()

    by_kind = {
        'dev': [
            'export CFLAGS="-I$(MNGR_%s_INC_DIR) $CFLAGS"' % my_name,
            'export LDFLAGS="-L$(MNGR_%s_LIB_DIR) $LDFLAGS"' % my_name,
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

            for x in [('(cp -R $(MNGR_%s_DIR)/%s/* $(INSTALL_DIR)/bin/ >& /dev/null) || true') % (func_name, x[1:]) for x in folders]:
                yield x
        else:
            for y in (('cp -R $(MNGR_%s_DIR)/%s $(INSTALL_DIR)/') % (func_name, x[1:]) for x in folders):
                yield y

    return y.to_v2({
        'code': '\n'.join(iter_ops()),
        'kind': 'split_part',
        'prepare': '\n'.join(by_kind[kind]),
        'deps': [func(info)],
        'codec': 'xz',
        'name': my_name.lower(),
    }, info)


REPACK_FUNCS = {
    'dev': ['/lib', '/include'],
    'run': ['/bin', '/sbin'],
    'doc': ['/share'],
    'log': ['/log'],
}


@y.singleton
def w_channel():
    return y.write_channel('new functions', 'spl')


@y.read_callback('new functions', 'spl')
def splitter(arg):
    repack = arg.get('repacks', REPACK_FUNCS)

    if not repack:
        return

    wc = w_channel()
    func = arg['func']
    kind = arg['kind']
    fn = func.__name__

    def do(k, folders):
        f1 = lambda info: split_part(k, folders, func, info)
        f1.__name__ = 'f1_' + fn + '_' + k
        f2 = lambda info: y.gen_func(f1, info, {})        
        f2.__name__ = fn + '_' + k

        return f2

    for k, folders in repack.items():
        f = do(k, folders)

        wc({'func': f, 'kind': kind + [k], 'fn': f.__name__, 'rfunc': func, 'repacks': None})
