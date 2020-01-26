def pkg_config_base(opts, deps, kind):
    return {
        'code': """
            source fetch "https://pkg-config.freedesktop.org/releases/pkg-config-{version}.tar.gz" 1
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared {opts}
            cd glib
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --with-libiconv=gnu --enable-static --disable-shared {opts} --srcdir=.
            $YMAKE -j $NTHRS
            cd ..
            $YMAKE -j $NTHRS
            $YMAKE install
        """.replace('{opts}', ' '.join(opts)),
        'version': '0.29.2',
        'meta': {
            'kind': kind,
            'depends': deps,
            'provides': [
                {'env': 'PKG_CONFIG', 'value': '{pkgroot}/bin/pkg-config'}
            ],
        },
    }


@y.ygenerator()
def pkg_config0():
    return pkg_config_base([], ['iconv', 'glib', 'slibtool'], ['box', 'tool'])


@y.ygenerator()
def pkg_config_int0():
    return pkg_config_base(['--with-internal-glib'], ['iconv', 'slibtool'], ['tool'])
