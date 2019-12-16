@y.ygenerator()
def gawk0():
    return {
        'code': """
             source fetch "https://mirror.tochlab.net/pub/gnu/gawk/gawk-{version}.tar.xz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --libexecdir=$IDIR/bin/awk_exec --disable-shared --enable-static --disable-extensions || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'version': '5.0.1',
        'meta': {
            'kind': ['box', 'tool'],
            'depends': ['iconv', 'intl', 'readline', 'libsigsegv', 'c++'],
            'soft': ['mpfr', 'gmp'],
        },
    }
