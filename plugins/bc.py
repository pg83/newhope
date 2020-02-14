@y.package
def bc0():
    return {
        'code': """
             source fetch "https://github.com/gavinhoward/bc/releases/download/{version}/bc-{version}.tar.xz" 1
             export LDFLAGS="$LDFLAGS $LIBS"
             export CFLAGS="$CFLAGS $LDFLAGS"
             $YSHELL ./configure.sh --prefix "$IDIR" -O3
             $YMAKE -j $THRS
             $YMAKE DESTDIR=$IDIR BINDIR=/bin install   
        """,
        'version': '2.5.3',
        'meta': {
            'kind': ['tool'],
            'depends': ['make', 'c'],
            'provides': [
                {'env': 'YBC', 'value': '{pkgroot}/bin/bc'},
            ],
        },
    }
