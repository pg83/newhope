@y.package
def unrar0():
    return {
        'code': """
             source fetch "http://www.rarlab.com/rar/unrarsrc-{version}.tar.gz" 0
             source add_strip
             cd unrar
             $YMAKE CC=$CC CXX=$CXX AR=$AR RANLIB=$RANLIB LDFLAGS="$LDFLAGS" CPPFLAGS="" CXXFLAGS="$CXXFLAGS" -f makefile
             mkdir -p $IDIR/bin
             install -v -m755 unrar $IDIR/bin
        """,
        'meta': {
            'kind': ['box', 'tool'],
            'depends': ['c++', 'make', 'c'],
            'provides': [
                {'env': 'YUNRAR', 'value': '{pkgroot}/bin/unrar'},
            ],
        },
    }
