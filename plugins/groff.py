#@y.package
def groff0():
    return {
        'code': """
             source fetch "http://ftp.gnu.org/gnu/groff/groff-{version}.tar.gz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'meta': {
            'kind': ['tool'],
            'depends': ['c++', 'texinfo','make', 'perl5', 'c'],
            'provides': [
                {'tool': 'TROFF', 'value': '{pkgroot}/bin/troff'},
            ],
        }
    }
