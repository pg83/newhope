@helper
def musl():
    return {
        'code': """
            #pragma cc

            export LDFLAGS=--static
            export CFLAGS=-O2
            export CROSS_COMPILE=$TOOL_CROSS_PREFIX

            ./configure --prefix=$(INSTALL_DIR) --enable-static --disable-shared && make && make install
        """,
        'src': 'https://www.musl-libc.org/releases/musl-1.1.23.tar.gz',
    }
