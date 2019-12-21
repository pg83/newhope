@y.ygenerator()
def dl0():
    return {
        'code': """
             source fetch "https://github.com/pg83/newhope/archive/{version}.zip" 0
             cd newhope* && cd support/libdl
             $YMAKE CXX="$CXX" CXXFLAGS="$CXXFLAGS" LDFLAGS="$LDFLAGS" LIBS="$LIBS" AR="$AR" NM="$NM" RANLIB="$RANLIB" DESTDIR="$IDIR" install
        """,
        'version': 'e785c9205424249765336f0f0fa92112119d615b',
        'meta': {
            'kind': ['library'],
            'depends': ['c++'],
            'provides': [
                {'lib': 'dl'},
            ],
        },
    }
