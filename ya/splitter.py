def gen_code(kind, folders):
    yield 'MDIR=$(dirname $3)'

    if kind == 'run':
        yield 'mkdir -p $IDIR/bin'

        for x in [('(cp -R $MDIR/%s/* $IDIR/bin/ 2> /dev/null) || true') % x[1:] for x in folders]:
            yield x

        yield 'cp $MDIR/install $IDIR/install'
        yield 'chmod +x $IDIR/install'
    else:
        for y in (('cp -R $MDIR/%s $IDIR/') % x[1:] for x in folders):
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
    nm = {}

    nm['kind'] = ['tool']

    def flt_provides():
        for p in m.get('provides', []):
            if 'lib' in p:
                continue

            if 'env' in p:
                e = p['env']

                if 'CFLAGS' in e or 'LIBS' in e:
                    continue

            yield p

    nm['provides'] = list(flt_provides())

    return nm


def split_meta(m, kind):
    if kind == 'run':
        return split_run_meta(m)

    return {
        'kind': ['library']
    }


def run_splitter(func, split):
    m = split_meta(func.code().get('meta', {}), split)

    m.update({
        'depends': [func.base],
        'undeps': ['musl', 'mimalloc', 'make']
    })

    return {
        'code': repacks()[split]['code'],
        'meta': m,
    }
