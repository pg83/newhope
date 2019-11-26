def gen_code(kind, folders):
    yield 'MDIR=$(dirname $3)'

    if kind == 'run':
        yield 'mkdir -p $IDIR/bin'

        for x in [('(cp -R $MDIR/%s/* $IDIR/bin/ 2> /dev/null) || true') % x[1:] for x in folders]:
            yield x
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


class SplitKind(object):
    def __init__(self, parent, kind):
        self.p = parent
        self.k = kind
        
        self.d = {
            'gen': self.p.arg['gen'],
            'base': self.p.arg['base'] + '-' + self.k,
            'kind': ['split', self.k],
            'code': self.run,
        }

    @y.cached_method
    def run(self, info):
        return y.gen_func(self.code, info)
        
    def split_part(self, info):
        return {
            'code': self.p.repacks[self.k]['code'],
            'kind': {'dev': ['library'], 'run': ['tool']}.get(self.k, []),
            'codec': 'xz',
            'deps': self.p.deps(info),
        }
    
    def code(self, info):
        return y.fix_pkg_name(y.to_v2(self.split_part(info), info), self.d)
    
        
class Splitter(object):
    def __init__(self, arg, repacks):
        self.arg = arg
        self.repacks = repacks

    @y.cached_method
    def deps(self, info):
        return [self.arg['code'](info)]

    def gen(self, kind):
        return SplitKind(self, kind).d

    
@y.pubsub.wrap    
def run_splitter(iface):
    yield y.EOP(y.ACCEPT('mf:new functions'), y.PROVIDES('mf:splitted'))

    for row in iface.iter_data():
        arg = row.data

        if not arg:
            yield y.FIN()

            return 
        
        arg = arg['func']
        repack = arg.get('repacks', repacks())
        
        if not repack:
            continue
    
        s = Splitter(arg, repack)
    
        for k in repack:
            yield y.ELEM({'func': s.gen(k)})

    yield y.EOP()

        
def pkg_splitter(arg, kind):
    return Splitter(arg, repacks()).gen(kind)['code']
