@y.package
def gzip0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/gzip/gzip-{version}.tar.gz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-gcc-warnings || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'meta': {
            'depends': ['make', 'c'],
            'provides': [
                {'tool': 'YGZIP', 'value': '{pkgroot}/bin/gzip'},
            ],
        },
    }
