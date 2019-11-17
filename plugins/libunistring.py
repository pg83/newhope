@y.ygenerator(tier=-2)
def libunistring0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/libunistring/libunistring-{version}.tar.xz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '0.9.10',
        'meta': {
            'kind': ['library'],
            'depends': [],
            'provides': [
                {'lib': 'unistring', 'configure': {'opt': '--with-libunistring-prefix={pkgroot}'}},
            ],
        },
    }
