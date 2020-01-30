@y.package
def dl0():
    return {
        'code': """
             source fetch "https://github.com/pg83/newhope/archive/{version}.zip" 0
             cd newhope* && cd support/libdl
             $YMAKE CXX="$CXX" CXXFLAGS="$CXXFLAGS" LDFLAGS="$LDFLAGS" LIBS="$LIBS" AR="$AR" NM="$NM" RANLIB="$RANLIB" DESTDIR="$IDIR" install
        """,
        'version': '670037f6c15db5c0b46b7452124bce8bcc2f9801',
        'meta': {
            'kind': ['library'],
            'depends': ['c++'],
            'provides': [
                {'lib': 'dl'},
            ],
        },
    }
