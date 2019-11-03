@ygenerator(tier=-1, kind=['core', 'dev', 'library'])
def mbedtls0():
    return {
        'code': """
            #pragma cc
            cat Makefile | grep -v 'DESTDIR=' > M && mv M Makefile
            CC=gcc $YMAKE -j2 programs lib && $YMAKE DESTDIR=$IDIR install
        """,
        'src': 'https://tls.mbed.org/download/mbedtls-2.16.3-apache.tgz',
        'version': '2.16.3',
    }
