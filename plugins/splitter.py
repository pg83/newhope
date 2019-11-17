def split_part(kind, folders, deps):
    def iter_ops():
        yield 'MDIR=$(dirname $3)'

        if kind == 'run':
            yield 'mkdir -p $IDIR/bin'

            for x in [('(cp -R $MDIR/%s/* $IDIR/bin/ 2> /dev/null) || true') % x[1:] for x in folders]:
                yield x
        else:
            for y in (('cp -R $MDIR/%s $IDIR/') % x[1:] for x in folders):
                yield y

    return {
        'code': '\n'.join(iter_ops()),
        'kind': [{'dev': 'library', 'run': 'tool'}.get(kind, 'unknown_role')],
        'codec': 'xz',
        'deps': deps,
    }


REPACK_FUNCS = {
    'dev': ['/lib', '/include'],
    'run': ['/bin', '/sbin'],
    'doc': ['/share'],
    'log': ['/log'],
}


@y.singleton
def w_channel():
    return y.write_channel('new functions', 'spl')


def do_gen(k, folders, arg):
    descr = {
        'gen': arg['gen'],
        'base': arg['base'] + '-' + k,
        'kind': ['split', k],
    }

    f1 = lambda info: y.fix_pkg_name(y.to_v2(split_part(k, folders, [arg['code'](info)]), info), descr)
    f2 = lambda info: y.gen_func(f1, info)

    descr['code'] = y.cached()(f2)

    return descr


@y.read_callback('new functions', 'spl')
def splitter(arg):
    arg = arg['func']
    repack = arg.get('repacks', REPACK_FUNCS)

    if not repack:
        return

    wc = w_channel()

    for k, folders in repack.items():
        wc({'func': do_gen(k, folders, arg)})
