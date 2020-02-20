@y.package
def quasar_m40():
    return {
        'code': """
               source fetch "http://haddonthethird.net/m4/m4-{version}.tar.bz2" 1
               $YMAKE -j $NTHRS CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS $LIBS" CC="$CC" m4 
               $YMAKE  PREFIX=/ DESTDIR="$IDIR" install
        """,
        'meta': {
            'kind': ['box', 'tool'],
            'depends': ['coreutils-boot', 'make', 'c'],
            'provides': [
                {'env': 'M4', 'value': '{pkgroot}/bin/m4'},
            ],
        },
    }
