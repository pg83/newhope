@ygenerator(tier=1, kind=['core', 'dev', 'library'])
def ncurses0():
    return {
        'code': """
            source fetch "https://ftp.gnu.org/pub/gnu/ncurses/ncurses-6.1.tar.gz" 1
            sed -i s/mawk// configure
            ./configure --prefix=$IDIR --without-shared --without-debug --without-ada --enable-widec --enable-overwrite --enable-ext-colors --enable-termcap
            $YMAKE -j2
            $YMAKE install
        """,
        'version': '6.1',
    }
