@y.ygenerator()
def quasar_m40():
    return {
        'code': """
               source fetch "http://haddonthethird.net/m4/m4-{version}.tar.bz2" 1
               $YMAKE -j $NTHRS CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS $LIBS" CC="$CC" PREFIX=/ DESTDIR="$IDIR" m4 
               $YMAKE install
        """,
        'version': '2',
        'meta': {
            'kind': ['box', 'tool'],
        },
    }
