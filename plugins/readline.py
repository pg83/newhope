@y.package
def readline0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/readline/readline-{version}.tar.gz" 1
             export CFLAGS="-Dxmalloc=rl_xmalloc -Dxrealloc=Drl_xrealloc $CFLAGS"
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared
             $YMAKE -j $NTHRS
             $YMAKE install 2>&1 | grep -v 'No such file or directory'
        """,
        'meta': {
            'kind': ['library'],
            'depends': ['ncurses', 'termcap', 'make', 'c'],
            'provides': [
                {'lib': 'readline', 'configure': {'opts': ['--with-installed-readline={pkgroot}', '--with-readline={pkgroot}']}},
            ],
        },
    }
