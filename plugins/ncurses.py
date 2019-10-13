@helper
def ncurses():
    return {
        'code': """
            #pragma cc

            sed -i s/mawk// configure
            ./configure --prefix=$(INSTALL_DIR) --without-shared --without-debug --without-ada --enable-widec --enable-overwrite
            make && make install
        """,
        'src': 'https://ftp.gnu.org/pub/gnu/ncurses/ncurses-6.1.tar.gz',
    }
