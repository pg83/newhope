@y.ygenerator(tier=2, kind=['box'])
def gawk0():
    return {
        'code': """
             source fetch "https://mirror.tochlab.net/pub/gnu/gawk/gawk-5.0.1.tar.xz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static --disable-extensions || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '5.0.1',
        'meta': {
            'depends': ['iconv', 'intl', 'readline', 'libsigsegv'],
            'soft': ['mpfr', 'gmp'],
        },
    }
