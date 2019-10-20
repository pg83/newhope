def curl0(info, name, deps, codec):
    return {
        'code': """
            ./configure --prefix=$(INSTALL_DIR) --with-mbedtls=$(MNGR_$(SS)_LIB_DIR) $(MNGR_MBEDTLS1_LIB_DIR) --enable-static --disable-shared && make && make install
        """.replace('$(SS)', name.upper()),
        'src': 'https://curl.haxx.se/snapshots/curl-7.67.0-20191011.tar.bz2',
        'deps': deps,
        'codec': codec,
        'prepare': '$(ADD_PATH)',
    }


@y.helper
def curl2(info):
    return curl0(info, "mbedtls2", [bestbox2(info), mbedtls2(info), make2(info)], 'gz')


@y.helper
def curl1(info):
    return curl0(info, "mbedtls1_dev", [bestbox1(info), mbedtls1_dev(info), make1(info), tar1(info), xz1(info)], 'xz')


@y.helper
def curl(info):
    return curl0(info, "mbedtls1_dev", [bestbox1(info), mbedtls1_dev(info), make1(info), tar1(info), xz1(info), musl1(info)], 'xz')


@y.splitter(folders=['/bin'])
def curl_runtime(info):
    return curl(info)
