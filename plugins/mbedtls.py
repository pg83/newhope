@ygenerator(tier=-1, kind=['core', 'dev', 'library'], cached=['deps', 'codec'])
def mbedtls0(deps, codec):
    return {
        'code': """
            #pragma cc
            cat Makefile | grep -v 'DESTDIR=' > M && mv M Makefile
            CC=gcc make -j2 programs lib && make DESTDIR=$IDIR install
        """,
        'src': 'https://tls.mbed.org/download/mbedtls-2.16.3-apache.tgz',
        'deps': deps,
        'codec': codec,
        'version': '2.16.3-apache',
    }
