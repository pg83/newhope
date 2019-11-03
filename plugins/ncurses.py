@ygenerator(tier=1, kind=['core', 'dev', 'library'])
def ncurses0():
    return {
        'code': """
            sed -i s/mawk// configure
            ./configure --prefix=$IDIR --without-shared --without-debug --without-ada --enable-widec --enable-overwrite
            $YMAKE -j2
            $YMAKE install
        """,
        'src': 'https://ftp.gnu.org/pub/gnu/ncurses/ncurses-6.1.tar.gz',
        'version': '6.1',
    }
