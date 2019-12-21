@y.ygenerator()
def dl0():
    return {
        'code': """
             source fetch "https://github.com/pg83/newhope/archive/{version}.zip" 0
             cd newhope* && cd support/libdl
             $YMAKE CXX="$CXX" CXXFLAGS="$CXXFLAGS" LDFLAGS="$LDFLAGS" LIBS="$LIBS" AR="$AR" NM="$NM" RANLIB="$RANLIB" DESTDIR="$IDIR" install
        """,
        'version': 'ab279c5728fb2760f82e090c08ac07bb88c595be',
        'meta': {
            'kind': ['library'],
            'depends': ['c++'],
            'provides': [
                {'lib': 'dl'},
            ],
        },
    }
