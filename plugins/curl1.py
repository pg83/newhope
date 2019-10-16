def curl0(info, deps, codec):
    return {
        'code': """
            ./configure --prefix=$(INSTALL_DIR) --with-mbedtls=$($(SS)_LIB_DIR) --enable-static --disable-shared && make && make install
        """.replace('$(SS)', xp('/deps/1/node/name').upper()),
        'src': 'https://curl.haxx.se/snapshots/curl-7.67.0-20191011.tar.bz2',
        'deps': deps,
        'codec': codec,
    }


@helper
def curl2(info):
    return curl0(info, [bestbox2(info), mbedtls2(info), make2(info)], 'gz')


@helper
def curl1(info):
    return curl0(info, [bestbox1(info), mbedtls1(info), make1(info), tar1(info), xz1(info)], 'xz')


@helper
def curl(info):
    return curl0(info, [bestbox1(info), mbedtls1(info), make1(info), tar1(info), xz1(info), musl1(info)], 'xz')
