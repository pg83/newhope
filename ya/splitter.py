def gen_code(kind, folders):
    yield 'MDIR=$(dirname $3)'

    if kind == 'run':
        yield 'mkdir -p $IDIR/bin'

        for x in [('(cp -R $MDIR/%s/* $IDIR/bin/ 2> /dev/null) || true') % x[1:] for x in folders]:
            yield x

        yield '(cp $MDIR/install $IDIR/install && chmod +x $IDIR/install) || true'
        yield '(cp $MDIR/run $IDIR/run && chmod +x $IDIR/run) || true'
    else:
        for y in (('cp -R $MDIR/%s $IDIR/ || true') % x[1:] for x in folders):
            yield y


@y.singleton
def repacks():
    by_kind = {
        'dev': ['/lib', '/include'],
        'run': ['/bin', '/sbin'],
        'doc': ['/share'],
        'log': ['/log'],
    }

    def iter():
        for k, v in by_kind.items():
            yield (k, {'folders': v, 'code': '\n'.join(gen_code(k, v))})

    return dict(iter())


@y.singleton
def repacks_keys():
    return sorted(list(repacks().keys()))


def split_run_meta(m):
    def flt_provides():
        for p in m.get('provides', []):
            if y.have_bin_fields(p):
                yield p

    return {
        'provides': list(flt_provides()),
    }


def split_dev_meta(m):
    def flt_provides():
        for p in m.get('provides', []):
            if y.have_lib_fields(p):
                yield p

    return {
        'provides': list(flt_provides()),
    }


def split_meta(m, kind):
    if kind == 'run':
        return split_run_meta(m)

    if kind == 'dev':
        return split_dev_meta(m)

    return {
        'kind': ['any']
    }


def run_splitter(func, split):
    m = split_meta(func.code().get('meta', {}), split)

    m.update({
        'depends': [func.base],
    })

    return {
        'code': repacks()[split]['code'],
        'meta': m,
    }
