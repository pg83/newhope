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
    m = y.dc(m)

    m.pop('depends', None)

    def flt_kind():
        for k in m.get('kind', []):
            if k == 'library':
                pass
            else:
                yield k

    m['kind'] = list(flt_kind())

    def flt_provides():
        for p in m.get('provides', []):
            if 'lib' in p:
                continue

            if 'env' in p:
                e = p['env']

                if 'CFLAGS' in e or 'LIBS' in e:
                    continue

            yield p

    m['provides'] = list(flt_provides())

    return m


def split_meta(m, kind):
    if kind == 'run':
        return split_run_meta(m)

    if kind in ('doc', 'log'):
        return {
            'flags': m.get('flags', []),
        }

    # TODO
    return m


class SplitKind(object):
    def __init__(self, parent, kind):
        self.p = parent
        self.k = kind

    @y.cached_method
    def run(self):
        return y.store_node(self.code())

    def split_part(self): 
        res = {
            'code': self.p.repacks[self.k]['code'],
            'kind': {'dev': ['library'], 'run': ['tool']}.get(self.k, []),
            'deps': [self.p.dep()],
            'meta': split_meta(self.p.meta(), self.k),
            'codec': self.p.node()['codec'],
        }

        res['meta']['kind'] = res.pop('kind')

        return res, self.p.arg['info']

    def code(self):
        return y.fix_v2(y.to_v2(*self.split_part()))


class Splitter(object):
    def __init__(self, arg, repacks):
        self.arg = arg
        self.repacks = repacks

    def dep(self):
        return self.arg['code']()

    def node(self):
        return y.restore_node_node(self.dep())

    def meta(self):
        return self.node().get('meta', {})

    def gen_code(self, kind):
        return SplitKind(self, kind).code()


def pkg_splitter(arg, kind):
    return Splitter(arg, repacks()).gen_code(kind)
