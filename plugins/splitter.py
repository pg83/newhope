def split_part(kind, folders, func, info):
    deps = [func(info)]
    my_name = (y.restore_node_node(deps[0])['name'] + '_' + kind).upper()

    def iter_ops():
        yield 'MDIR=$(dirname $3)'

        if kind == 'run':
            yield 'mkdir -p $IDIR/bin'

            for x in [('(cp -R $MDIR/%s/* $IDIR/bin/ 2> /dev/null) || true') % x[1:] for x in folders]:
                yield x
        else:
            for y in (('cp -R $MDIR/%s $IDIR/') % x[1:] for x in folders):
                yield y

    return y.to_v2({
        'code': '\n'.join(iter_ops()),
        'kind': [{'dev': 'library', 'run': 'tool'}.get(kind, 'unknown_role')],
        'codec': 'xz',
        'deps': deps, 
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
    gf = y.gen_func

    def do(k, folders):
        f1 = lambda info: split_part(k, folders, func, info)
        f1.__name__ = 'f1_' + fn + '_' + k
        f2 = lambda info: gf(f1, info)        
        f2.__name__ = fn + '_' + k
        #f3 = y.cached()(f2)
        #f3.__name__ = fn + '_' + k

        return f2

    for k, folders in repack.items():
        f = do(k, folders)

        wc({'func': f, 'kind': kind + [k], 'fn': f.__name__, 'rfunc': func, 'repacks': None})
