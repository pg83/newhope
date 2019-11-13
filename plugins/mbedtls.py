@y.ygenerator(tier=-1, kind=['core', 'dev', 'library'])
def mbedtls0():
    return {
        'code': """
            source fetch "https://tls.mbed.org/download/mbedtls-2.16.3-apache.tgz" 1
            #pragma cc
            cat Makefile | grep -v 'DESTDIR=' > M && mv M Makefile
            CC=gcc $YMAKE -j2 programs lib && $YMAKE DESTDIR=$IDIR install
        """,
        'version': '2.16.3',
        'meta': {
            'depends': [],
            'provides': [
                {'lib': 'mbedtls', 'configure': {'opt': '--with-mbedtls={pkg_root}'}},
            ],
        },
    }
