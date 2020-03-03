@y.package
def libunistring0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/libunistring/libunistring-{version}.tar.xz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'meta': {
            'depends': ['iconv', 'xz', 'make', 'c'],
            'provides': [
                {'lib': 'unistring'},
                {'configure': '--with-libunistring-prefix={pkgroot}'},
            ],
        },
    }
