@y.package
def mpdecimal0():
    return {
        'code': """
             source fetch "http://deb.debian.org/debian/pool/main/m/mpdecimal/mpdecimal_{version}.orig.tar.gz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static || exit 1
             (cd libmpdec && $YMAKE -j $NTHRS libmpdec.a)
             touch libmpdec/libmpdec.so.2.4.2
             $YMAKE install
             rm -rf $IDIR/lib/*.so.*
             rm -rf $IDIR/lib/*.so
        """,
        'version': '2.4.2',
        'meta': {
            'kind': ['library'],
            'depends': ['make', 'c'],
            'provides': [
                {'lib': 'mpdec'},
            ],
        },
    }
