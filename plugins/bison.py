@y.package
def bison0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/bison/bison-{version}.tar.xz" 1
             export CFLAGS="-Daccept=bison_accept -Dxcalloc=bison_xcalloc -Dxmalloc=bison_xmalloc -Dxmemdup=bison_xmemdup -Dxnmalloc=bison_xnmalloc -Dxrealloc=bison_xrealloc -Dxstrdup=bison_xstrdup -Dxzalloc=bison_xzalloc  $CFLAGS"
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static --enable-relocatable || exit 1
             $YMAKE -j $NTHRS || true
             $YMAKE || true
             $YMAKE
             $YMAKE install
        """,
        'meta': {
            'depends': ['c++', 'm4', 'iconv', 'intl', 'xz', 'perl5', 'make', 'c']
        },
    }

