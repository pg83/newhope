@y.ygenerator(tier=0, kind=['core', 'library', 'tool', 'box'])
def readline0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/readline/readline-8.0.tar.gz" 1
             $YSHELL ./configure --prefix=$IDIR --enable-static --disable-shared
             $YMAKE -j2
             $YMAKE install 2>&1 | grep -v 'No such file or directory'
        """,
        'version': '8.0',
        'meta': {
            'depends': ['ncurses'],
            'provides': [
                {'lib': 'readline', 'configure': {'opt': '--with-installed-readline={pkg_root}'}},
            ],
        },
    }
