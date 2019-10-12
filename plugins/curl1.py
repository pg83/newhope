@helper
def curl1():
    return {
        'code': """
            #pragma cc

            $(FETCH_URL)
            ./configure --prefix=$(INSTALL_DIR) --with-mbedtls=$(MBEDTLS1_LIB_DIR) --enable-static --disable-shared && make && make install
        """,
        'src': 'https://curl.haxx.se/snapshots/curl-7.67.0-20191011.tar.bz2',
    }
