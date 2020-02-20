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
            'kind': ['library'],
            'depends': ['iconv', 'xz', 'make', 'c'],
            'provides': [
                {'lib': 'unistring', 'configure': {'opt': '--with-libunistring-prefix={pkgroot}'}},
            ],
        },
    }
