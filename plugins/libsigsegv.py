@y.package
def libsigsegv0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/libsigsegv/libsigsegv-{version}.tar.gz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'meta': {
            'depends': ['make', 'c'],
            'provides': [
                {'lib': 'sigsegv', 'configure': {'opt': '--with-libsigsegv-prefix={pkgroot}'}},
            ],
        },
    }
