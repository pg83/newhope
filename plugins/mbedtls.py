def mbedtls0(deps, codec):
    return {
        'code': """
            #pragma cc
            cat Makefile | grep -v 'DESTDIR=' > M && mv M Makefile
            CC=gcc make programs lib && make DESTDIR=$(INSTALL_DIR) install
        """,
        'src': 'https://tls.mbed.org/download/mbedtls-2.16.3-apache.tgz',
        'deps': deps,
        'codec': codec,
    }


@y.helper
def mbedtls2(info):
    return mbedtls0([make2(info), bestbox2(info)], 'gz')


@y.helper
def mbedtls1(info):
    return mbedtls0([make1(info), bestbox1(info), tar1(info), xz1(info)], 'xz')


@y.splitter(folders=['/lib', '/include'])
def mbedtls1_dev(info):
    return mbedtls1(info)
