@y.package
def jemalloc0():
    return {
        'code': """
             source fetch "https://github.com/jemalloc/jemalloc/releases/download/{version}/jemalloc-{version}.tar.bz2" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared --disable-cxx --disable-prof --disable-libdl || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'meta': {
            'kind': ['library'],
            'depends': ['make', 'c'],
            'contains': ['mimalloc'],
            'provides': [
                {'lib': 'jemalloc'},
            ],
        },
    }
