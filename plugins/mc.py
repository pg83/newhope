@y.ygenerator(tier=3, kind=['base', 'program'])
def mc0():
    return {
        'code': """
             source fetch "http://ftp.midnight-commander.org/mc-4.8.23.tar.xz" 1
             $YSHELL ./configure --prefix=$IDIR --disable-shared --enable-static --with-screen=ncurses  || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '4.8.23',
        'meta': {
            'depends': ['intl', 'iconv', 'glib', 'ncurses', 'slang'],
        }
    }
