@y.ygenerator()
def coreutils0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/coreutils/coreutils-{version}.tar.xz" 1 
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --libexecdir=$IDIR/bin --without-gmp || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '8.31',
        'meta': {
            'kind': ['box', 'tool'],
            'depends': ['iconv', 'intl'],
            'soft': ['openssl'],
        },
    }
