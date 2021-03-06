@y.package
def gawk0():
    return {
        'code': """
             source fetch "https://mirror.tochlab.net/pub/gnu/gawk/gawk-{version}.tar.xz" 1
             source fake_binutils

             export CFLAGS="-Derr=gawk_err -Dxmalloc=gawk_xmalloc -Dxrealloc=Dgawk_xrealloc -Dregcomp=gawk_regcomp -Dregfree=gawk_regfree  $CFLAGS"

             $YSHELL ./configure $COFLAGS --prefix=$IDIR --libexecdir=$IDIR/bin/awk_exec --disable-shared --enable-static --disable-extensions || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'meta': {
            'depends': ['iconv', 'intl', 'readline', 'libsigsegv', 'c++', 'make', 'c'],
            'soft': ['mpfr', 'gmp'],
        },
    }
