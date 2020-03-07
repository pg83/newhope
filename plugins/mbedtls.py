@y.package
def mbedtls0():
    return {
        'code': '''
            source fetch "https://tls.mbed.org/download/mbedtls-{version}.tgz" 1
            cat Makefile | grep -v 'DESTDIR=' > M && mv M Makefile
            $YMAKE -j $NTHRS programs lib && $YMAKE DESTDIR=$IDIR install
            $YUPX $IDIR/bin/* || true
        ''',
        'meta': {
            'depends': ['upx', 'crt', 'make', 'c'],
            'provides': [
                {'lib': 'mbedtls'},
                {'configure': '--with-mbedtls={pkgroot}'},
                {'env': 'MBEDTLS_ROOT', 'value': '"{pkgroot}"'},
            ],
        },
    }
