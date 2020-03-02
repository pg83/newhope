LIB_FIELDS = {'lib', 'extra', 'configure', 'env'}
BIN_FIELDS = {'tool'}


def have_fields(p, fields):
    return fields & frozenset(p.keys())


def have_lib_fields(p):
    return have_fields(p, LIB_FIELDS)


def have_bin_fields(p):
    return have_fields(p, BIN_FIELDS)


def meta_to_build(meta):
    def iter():
        kind = set(meta['kind'])

        is_lib = 'library' in kind
        is_bin = 'tool' in kind

        yield 'export CMAKE_PREFIX_PATH="{pkgroot}:$CMAKE_PREFIX_PATH"'

        if is_lib:
            yield 'export CPPFLAGS="$CPPFLAGS -I{pkgroot}/include"'
            yield 'export LDFLAGS="-L{pkgroot}/lib $LDFLAGS"'
            yield 'export PKG_CONFIG_PATH="{pkgroot}/lib/pkgconfig:$PKG_CONFIG_PATH"'

        if is_bin:
            yield 'export PATH="{pkgroot}/bin:$PATH"'

        for p in meta.get('provides', []):
            if is_lib and have_lib_fields(p):
                if 'lib' in p:
                    yield 'export LIBS="{lib} $LIBS"'.format(lib='-l' + p['lib'])

                if 'extra' in p:
                    for e in p['extra']:
                        if 'libs' in e:
                            yield 'export LIBS="{extra} $LIBS"'.format(extra=e['libs'])

                        if 'ipath' in e:
                            yield 'export CPPFLAGS="$CPPFLAGS -I{ipath}"'.format(ipath=e['ipath'])

                if 'configure' in p:
                    cfg = p['configure']

                    if isinstance(cfg, str):
                        yield 'export COFLAGS="$COFLAGS {opt}"'.format(opt=cfg)
                    else:
                        if 'opt' in cfg:
                            yield 'export COFLAGS="$COFLAGS {opt}"'.format(opt=cfg['opt'])

                        if 'opts' in cfg:
                            for o in cfg['opts']:
                                yield 'export COFLAGS="$COFLAGS {opt}"'.format(opt=o)

                if 'env' in p:
                    yield 'export {k}={v}'.format(k=p['env'], v=p['value'])

            if is_bin and have_bin_fields(p):
                if 'tool' in p:
                    yield 'export {k}={v}'.format(k=p['tool'], v=p['value'])

    return '\n'.join(iter()) + '\n'
