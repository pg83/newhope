@y.package
def zlib0():
    return {
        'code': """
            source fetch "http://zlib.net/zlib-{version}.tar.gz" 1
            export LDFLAGS="$LDFLAGS $LIBS"
            export TEST_LDFLAGS="$LDFLAGS -L. libz.a"
            $YSHELL ./configure $COFLAGS --static --64 --prefix=$IDIR || exit 1
            $YMAKE -j $NTHRS TEST_LDFLAGS="$TEST_LDFLAGS"
            $YMAKE install
        """,
        'version': '1.2.11',
        'meta': {
            'kind': ['library'],
            'depends': [],
            'provides': [
                {'lib': 'z', 'configure': {'opt': '--with-z={pkgroot}'}},
                {'env': 'ZLIB_CFLAGS', 'value': '"-I{pkgroot}/include"'},
                {'env': 'ZLIB_LIBS', 'value': '"-L{pkgroot}/lib -lz"'},
            ],
        },
    }
