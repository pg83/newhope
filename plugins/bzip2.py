@y.package
def bzip20():
    return {
        'code': """
            source fetch "https://sourceware.org/pub/bzip2/bzip2-{version}.tar.gz" 1
            $YMAKE -j $NTHRS CC=$CC AR=$AR RANLIB=$RANLIB LDFLAGS="$LDFLAGS $LIBS" CFLAGS="$CFLAGS" PREFIX="$IDIR" install
        """,
        'meta': {
            'depends': ['make', 'c'],
            'provides': [
                {'lib': 'bz2'},
                {'tool': 'YBZIP2', 'value': '{pkgroot}/bin/bzip2'},
            ],
        },
    }
