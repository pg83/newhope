@y.package
def curl0():
    return {
        'code': """
            source fetch "https://curl.haxx.se/download/curl-7.67.0.tar.xz" 1
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared
            $YMAKE -j $NTHRS
            $YMAKE install
        """,
        'version': '7.67.0-20191011',
        'meta': {
            'kind': ['box', 'tool'],
            'depends': ['openssl', 'libidn2', 'libmetalink'],
            'provides': [
                {'env': 'CURL', 'value': '{pkgroot}/bin/curl'},
            ],
        },
    }
