@y.package
def expat0():
    return {
        'code': """
             source fetch "https://github.com/libexpat/libexpat/releases/download/R_{_version_}/expat-{version}.tar.bz2" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --without-examples --enable-static --disable-shared || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'version': '2.2.9',
        'meta': {
            'kind': ['library'],
            'depends': ['make', 'c'],
            'provides': [
                {'lib': 'expat', 'configure': {'opt': '--with-expat={pkgroot}'}},
            ],
        },
    }
