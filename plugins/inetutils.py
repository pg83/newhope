@y.package
def inetutils0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/inetutils/inetutils-{version}.tar.xz" 1
             export CFLAGS="-Dtimeout=inet_timeout $CFLAGS"
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static --disable-rcp --disable-rsh --disable-rlogin --disable-rexec || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'meta': {
            'kind': ['tool'],
            'depends': ['intl', 'iconv', 'ncurses', 'readline'],
        },
    }
