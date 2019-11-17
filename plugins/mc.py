@y.ygenerator(tier=3)
def mc0():
    return {
        'code': """
             source fetch "http://ftp.midnight-commander.org/mc-{version}.tar.xz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static --with-screen=ncurses  || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '4.8.23',
        'meta': {
            'kind': ['program'],
            'depends': ['intl', 'iconv', 'glib', 'ncurses', 'slang'],
        }
    }
