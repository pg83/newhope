@y.options()
def ncurses(info):
    return to_v2({
        'code': """
            sed -i s/mawk// configure
            ./configure --prefix=$(INSTALL_DIR) --without-shared --without-debug --without-ada --enable-widec --enable-overwrite
            make && make install
            $(MOVE_LOG) config.log
        """,
        'src': 'https://ftp.gnu.org/pub/gnu/ncurses/ncurses-6.1.tar.gz',
        'deps': devtools(info),
    }, info)
