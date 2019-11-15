def is_compat(a, b):
    return True


def meta_to_build(meta, platform, target):
    def iter():
        if 'kind' not in meta:
            meta['kind'] = []

        kind = set(meta['kind'])

        if 'box' in kind:
            kind.add('tool')

        if 'compression' in kind:
            kind.add('tool')

        if 'provides' in meta:
            kind.add('library')

        if 'library' in kind:
            yield 'export CFLAGS="-I{pkgroot}/include $CFLAGS"'
            yield 'export LDFLAGS="-L{pkgroot}/lib $LDFLAGS"'
            yield 'export PKG_CONFIG_PATH="{pkgroot}/lib/pkgconfig:$PKG_CONFIG_PATH"'
            
        if 'tool' in kind:
            yield 'export PATH="{pkgroot}/bin:$PATH"'

        for p in meta.get('provides', []):
            if 'lib' in p:
                yield 'export LIBS="$LIBS {lib}"'.format(lib='-l' + p['lib'])

            if 'extra' in p:
                for e in p['extra']:
                    if is_compat(e, platform):
                        yield 'export LIBS="$LIBS {extra}"'.format(extra=e['libs'])

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
