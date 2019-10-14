@helper
def pkg_config(info):
    return {
        'code': """
            #pragma cc

            LDFLAGS=--static ./configure --prefix=$(INSTALL_DIR) --with-internal-glib --enable-static --disable-shared && make && make install
        """,
        'src': 'https://pkg-config.freedesktop.org/releases/pkg-config-0.29.2.tar.gz',
        'deps': devtools(info),
    }
