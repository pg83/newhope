@y.ygenerator()
def mbedtls0():
    return {
        'code': """
            source fetch "https://tls.mbed.org/download/mbedtls-{version}-apache.tgz" 1
            #pragma cc
            cat Makefile | grep -v 'DESTDIR=' > M && mv M Makefile
            $YMAKE -j4 CC=$CC AR=$AR RANLIB=$RANLIB CFLAGS="$CFLAGS" LIBS="$LIBS" LDFLAGS="$LDFLAGS" DESTDIR=$IDIR programs lib install
        """,
        'version': '2.16.3',
        'meta': {
            'kind': ['library'],
            'depends': [],
            'provides': [
                {'lib': 'mbedtls', 'configure': {'opt': '--with-mbedtls={pkgroot}'}},
            ],
        },
    }
