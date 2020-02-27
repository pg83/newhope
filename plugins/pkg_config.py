def pkg_config_base(cflags, opts, deps):
    return {
        'code': """
            source fetch "https://pkg-config.freedesktop.org/releases/pkg-config-{version}.tar.gz" 1 
            export CFLAGS="{cflags} $CFLAGS" 
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared {opts}
            cd glib
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --with-libiconv=gnu --enable-static --disable-shared {opts} --srcdir=.
            $YMAKE -j $NTHRS
            cd ..
            $YMAKE -j $NTHRS
            $YMAKE install
        """.replace('{opts}', ' '.join(opts)).replace('{cflags}', cflags),
        'version': y.package_versions()['pkg-config'],
        'meta': {
            'kind': ['tool'],
            'depends': deps + ['iconv', 'file', 'make', 'c'],
            'provides': [
                {'tool': 'PKG_CONFIG', 'value': '{pkgroot}/bin/pkg-config'}
            ],
        },
    }


@y.package
def pkg_config0():
    return pkg_config_base('', [], ['glib'])


@y.package
def pkg_config_int0():
    return pkg_config_base('-Iglib -Iglib/glib', ['--with-internal-glib'], [])
