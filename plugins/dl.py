@y.ygenerator()
def dl0():
    return {
        'code': """
             source fetch "https://github.com/pg83/newhope/archive/{version}.zip" 0
             cd newhope* && cd support/libdl
             $YMAKE CXX="$CXX" CXXFLAGS="$CXXFLAGS" LDFLAGS="$LDFLAGS" LIBS="$LIBS" AR="$AR" NM="$NM" RANLIB="$RANLIB" DESTDIR="$IDIR" install
        """,
        'version': '381c721ad9da3099ac1825be3dfeec7041ab1714',
        'meta': {
            'kind': ['library'],
            'depends': ['c++'],
            'provides': [
                {'lib': 'dl'},
            ],
        },
    }
