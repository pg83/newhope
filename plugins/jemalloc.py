@y.ygenerator()
def jemalloc0():
    return {
        'code': """
             source fetch "https://github.com/jemalloc/jemalloc/releases/download/{version}/jemalloc-{version}.tar.bz2" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared --disable-cxx --disable-prof --disable-libdl || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'version': '5.2.1',
        'meta': {
            'kind': ['library'],
            'depends': ['make-boot'],
            'provides': [
                {'lib': 'jemalloc'},
            ],
        },
    }
