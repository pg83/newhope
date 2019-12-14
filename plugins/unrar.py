@y.ygenerator()
def unrar0():
    return {
        'code': """
             source fetch "http://www.rarlab.com/rar/unrarsrc-{version}.tar.gz" 0
             cd unrar
             $YMAKE CC=$CC CXX=$CXX AR=$AR RANLIB=$RANLIB LDFLAGS="$LDFLAGS" CXXFLAGS="$CXXFLAGS" -f makefile
             mkdir -p $IDIR/bin
             install -v -m755 unrar $IDIR/bin
        """,
        'version': '5.8.3',
        'meta': {
            'kind': ['compression', 'tool'],
            'depends': ['c++'],
            'provides': [
                {'env': 'YUNRAR', 'value': '{pkgroot}/bin/unrar'},
            ],
        },
    }
