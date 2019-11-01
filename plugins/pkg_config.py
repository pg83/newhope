@ygenerator(tier=2, kind=['core', 'dev', 'tool'], cached=['deps'])
def pkg_config0(deps):
    return {
        'code': """
            ./configure --prefix=$IDIR --with-internal-glib --enable-static --disable-shared
            $YMAKE
            $YMAKE install
        """,
        'src': 'https://pkg-config.freedesktop.org/releases/pkg-config-0.29.2.tar.gz',
        'deps': deps,
        'prepare': '$(ADD_PATH)',
        'version': '0.29.2',
    }
