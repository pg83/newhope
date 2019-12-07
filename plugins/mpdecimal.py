@y.ygenerator()
def mpdecimal0():
    return {
        'code': """
             source fetch "http://deb.debian.org/debian/pool/main/m/mpdecimal/mpdecimal_{version}.orig.tar.gz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j2
             $YMAKE install
             rm -rf $IDIR/lib/*.so.*
             rm -rf $IDIR/lib/*.so
        """,
        'version': '2.4.2',
        'meta': {
            'kind': ['library'],
            'provides': [
                {'lib': 'mpdec'},
            ],
        },
    }
