@helper
def xz():
    return {
        'code': """
            export PATH=$(BUSYBOX1_BIN_DIR):$PATH

            ./configure --prefix=$(INSTALL_DIR) --disable-shared --enable-static && make && make install

            #pragma cc
            #pragma manual deps
        """,
        'src': 'https://downloads.sourceforge.net/project/lzmautils/xz-5.2.4.tar.gz',
    }
