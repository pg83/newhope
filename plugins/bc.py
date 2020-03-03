@y.package
def bc0():
    return {
        'code': """
             source fetch "https://github.com/gavinhoward/bc/releases/download/{version}/bc-{version}.tar.xz" 1
             export LDFLAGS="$LDFLAGS $LIBS"
             export CFLAGS="$CFLAGS $LDFLAGS"
             $YSHELL ./configure.sh --prefix "$IDIR" -O3
             $YMAKE -j $NTHRS
             $YMAKE DESTDIR=$IDIR BINDIR=/bin install   
        """,
        'meta': {
            'depends': ['make', 'c'],
            'provides': [
                {'tool': 'YBC', 'value': '{pkgroot}/bin/bc'},
            ],
        },
    }
