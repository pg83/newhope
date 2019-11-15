def pkg_config_base(opts, deps):
    return {
        'code': """
            source fetch "https://pkg-config.freedesktop.org/releases/pkg-config-0.29.2.tar.gz" 1
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared {opts}
            $YMAKE
            $YMAKE install
        """.format(opts=' '.join(opts)),
        'version': '0.29.2',
        'meta': {
            'depends': deps,
            'provides': [
                {'env': 'PKG_CONFIG', 'value': '{pkgroot}/bin/pkg-config'}
            ],
        },
    }


@y.ygenerator(tier=0, kind=['box'])
def pkg_config0():
    return pkg_config_base([], ['iconv', 'glib'])


@y.ygenerator(tier=0, kind=[])
def pkg_config_int0():
    return pkg_config_base(['--with-internal-glib'], ['iconv'])
