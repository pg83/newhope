@ygenerator(tier=1, kind=['core', 'dev', 'library'], cached=['deps'])
def ncurses0(deps):
    return {
        'code': """
            sed -i s/mawk// configure
            ./configure --prefix=$IDIR --without-shared --without-debug --without-ada --enable-widec --enable-overwrite
            $YMAKE -j2
            $YMAKE install
        """,
        'src': 'https://ftp.gnu.org/pub/gnu/ncurses/ncurses-6.1.tar.gz',
        'deps': deps,
        'version': '6.1',
    }
