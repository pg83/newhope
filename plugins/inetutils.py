#@y.package
def inetutils0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/inetutils/inetutils-{version}.tar.xz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'version': '1.9.4',
        'meta': {
            'kind': ['tool'],
            'depends': ['intl', 'iconv', 'ncurses', 'readline', 'libedit'],
        },
    }
