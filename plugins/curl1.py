def curl0(info, deps, codec):
    return {
        'code': """
            ./configure --prefix=$(INSTALL_DIR) --with-mbedtls=$(MNGR_$(SS)_LIB_DIR) --enable-static --disable-shared && make && make install
        """.replace('$(SS)', dep_name(deps[1]).upper()),
        'src': 'https://curl.haxx.se/snapshots/curl-7.67.0-20191011.tar.bz2',
        'deps': deps,
        'codec': codec,
        'prepare': '$(ADD_PATH)',
    }


@y.options()
def curl2(info):
    return curl0(info, [bestbox2_run(info), mbedtls2_dev(info), make2_run(info)], 'gz')


@y.options()
def curl1(info):
    return curl0(info, [bestbox1_run(info), mbedtls1_dev(info), make1_run(info), tar1_run(info), xz1_run(info)], 'xz')


@y.options()
def curl(info):
    return curl0(info, [bestbox1_run(info), mbedtls1_dev(info), make1_run(info), tar1_run(info), xz1_run(info)], 'xz')
