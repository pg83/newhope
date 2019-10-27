def mbedtls0(info, deps, codec):
    return to_v2({
        'code': """
            #pragma cc
            cat Makefile | grep -v 'DESTDIR=' > M && mv M Makefile
            CC=gcc make -j2 programs lib && make DESTDIR=$(INSTALL_DIR) install
        """,
        'src': 'https://tls.mbed.org/download/mbedtls-2.16.3-apache.tgz',
        'deps': deps,
        'codec': codec,
    }, info)


@y.options()
def mbedtls2(info):
    return mbedtls0(info, [make2_run(info), bestbox2_run(info)], 'gz')


@y.options()
def mbedtls1(info):
    return mbedtls0(info, [make1_run(info), bestbox1_run(info), tar1_run(info), xz1_run(info)], 'xz')
