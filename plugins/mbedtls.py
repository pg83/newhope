def mbedtls0(deps, codec):
    return {
        'code': """
            rm -rf /usr/local
            make programs lib && make install
            cd /usr/local && mv * $(INSTALL_DIR)/
        """,
        'src': 'https://tls.mbed.org/download/mbedtls-2.16.3-apache.tgz',
        'deps': deps,
        'codec': codec,
    }


@helper
def mbedtls2(info):
    return mbedtls0([make2(info), bestbox2(info)], 'gz')


@helper
def mbedtls1(info):
    return mbedtls0([make1(info), bestbox1(info), tar1(info), xz1(info)], 'xz')
