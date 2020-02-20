@y.package
def curl0():
    return {
        'code': """
            source fetch "https://curl.haxx.se/download/curl-7.67.0.tar.xz" 1
            export CFLAGS="$OPENSSL_INCLUDES $CFLAGS"
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared
            $YMAKE -j $NTHRS
            $YMAKE install
        """,
        'meta': {
            'kind': ['box', 'tool'],
            'depends': ['openssl', 'libidn2', 'libmetalink', 'make', 'c'],
            'provides': [
                {'env': 'CURL', 'value': '{pkgroot}/bin/curl'},
            ],
        },
    }
