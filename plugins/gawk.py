@y.package
def gawk0():
    return {
        'code': """
             source fetch "https://mirror.tochlab.net/pub/gnu/gawk/gawk-{version}.tar.xz" 1

             ln -s $AR ./ar
             export PATH="$(pwd):$PATH"
             export CFLAGS="-Derr=gawk_err -Dxmalloc=gawk_xmalloc -Dxrealloc=Dgawk_xrealloc -Dregcomp=gawk_regcomp -Dregfree=gawk_regfree  $CFLAGS"

             $YSHELL ./configure $COFLAGS --prefix=$IDIR --libexecdir=$IDIR/bin/awk_exec --disable-shared --enable-static --disable-extensions || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'version': '5.0.1',
        'meta': {
            'kind': ['box', 'tool'],
            'depends': ['iconv', 'intl', 'readline', 'libsigsegv', 'c++', 'make', 'c'],
            'soft': ['mpfr', 'gmp'],
        },
    }
