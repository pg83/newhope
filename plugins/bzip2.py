@y.ygenerator()
def bzip20():
    return {
        'code': """
            source fetch "https://sourceware.org/pub/bzip2/bzip2-{version}.tar.gz" 1
            $YMAKE -j $NTHRS CC=$CC AR=$AR RANLIB=$RANLIB LDFLAGS="$LDFLAGS $LIBS" CFLAGS="$CFLAGS" PREFIX="$IDIR" install
        """,
        'version': '1.0.8',
        'meta': {
            'kind': ['library', 'box', 'tool'],
            'provides': [
                {'lib': 'bz2'},
                {'env': 'YBZIP2', 'value': '{pkgroot}/bin/bzip2'},
            ],
        },
    }
