@y.ygenerator()
def readline0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/readline/readline-{version}.tar.gz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared
             $YMAKE -j $NTHRS
             $YMAKE install 2>&1 | grep -v 'No such file or directory'
        """,
        'version': '8.0',
        'meta': {
            'kind': ['library'],
            'depends': ['ncurses', 'termcap'],
            'provides': [
                {'lib': 'readline', 'configure': {'opts': ['--with-installed-readline={pkgroot}', '--with-readline={pkgroot}']}},
                #{'lib': 'history'},
            ],
        },
    }
