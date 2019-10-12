@helper
def tar():
    return {
        'code': """
        export PATH=$(BUSYBOX1_BIN_DIR):$(XZ_BIN_DIR):$PATH

        $(FETCH_URL) FORCE_UNSAFE_CONFIGURE=1 ./configure --prefix=$(INSTALL_DIR) && make && make install

        #pragma cc
        #pragma manual deps
        """,
        'src': 'https://ftp.gnu.org/gnu/tar/tar-1.32.tar.gz',
    }
