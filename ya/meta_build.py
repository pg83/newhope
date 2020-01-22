def is_dict(v):
    try:
        v['']
    except KeyError:
        return True
    except Exception:
        return False


def is_list(v):
    try:
        return v[:0] == []
    except TypeError:
        pass

    return False

def to_platform(k, v):
    if k == 'os':
        return {'os': v}

    return v


class Remove(Exception):
    pass


class Replace(Exception):
    def __init__(self, v):
        self.value = v


@y.cached()
def is_compat_0(pl, k, v):
    return is_compat(pl, to_platform(k, v))


def platform_slice(vv, pl):
    def fix_dict(v):
        for k, l in v.items():
            if k in ('os', 'platform'):
                if is_compat_0(pl, k, l):
                    if 'value' in v:
                        raise Replace(v['value'])
                    else:
                        pass
                else:
                    raise Remove()
            else:
                for x in do(l):
                    yield k, x

    def fix_list(l):
        for x in l:
            for y in do(x):
                yield y
    
    def do(v):
        if is_dict(v):
            try:
                yield dict(fix_dict(v))
            except Remove:
                return
            except Replace as r:
                for y in do(r.value):
                    yield y
        elif is_list(v):
            yield list(fix_list(v))
        else:
            yield v

    for x in do(vv):
        return x


def is_compat(a, b):
    for x in b:
        if x not in a:
            return False

        if a[x] != b[x]:
            return False

    return True


def meta_to_build(meta):
    def iter():
        kind = set(meta['kind'])
        
        is_lib = 'library' in kind
        is_bin = 'tool' in kind

        yield 'export CMAKE_PREFIX_PATH="{pkgroot}:$CMAKE_PREFIX_PATH"'
        
        if is_lib:
            #yield 'export CFLAGS="-I{pkgroot}/include $CFLAGS"'
            yield 'export CPPFLAGS="$CPPFLAGS -I{pkgroot}/include"'
            yield 'export LDFLAGS="-L{pkgroot}/lib $LDFLAGS"'
            yield 'export PKG_CONFIG_PATH="{pkgroot}/lib/pkgconfig:$PKG_CONFIG_PATH"'

        if is_bin:
            yield 'export PATH="{pkgroot}/bin:$PATH"'

        for p in meta.get('provides', []):
            if is_lib:
                if 'lib' in p:
                    yield 'export LIBS="{lib} $LIBS"'.format(lib='-l' + p['lib'])

                if 'extra' in p:
                    for e in p['extra']:
                        if 'libs' in e:
                            yield 'export LIBS="{extra} $LIBS"'.format(extra=e['libs'])

                        if 'ipath' in e:
                            yield 'export CPPFLAGS="$CPPFLAGS -I{ipath}"'.format(ipath=e['ipath'])
                            #yield 'export CFLAGS="-I{ipath} $CFLAGS"'.format(ipath=e['ipath'])

                if 'configure' in p:
                    cfg = p['configure']

                    if 'opt' in cfg:
                        yield 'export COFLAGS="$COFLAGS {opt}"'.format(opt=cfg['opt'])

                    if 'opts' in cfg:
                        for o in cfg['opts']:
                            yield 'export COFLAGS="$COFLAGS {opt}"'.format(opt=o)

            if 'env' in p:
                yield 'export {k}={v}'.format(k=p['env'], v=p['value'])

    return '\n'.join(iter()) + '\n'
