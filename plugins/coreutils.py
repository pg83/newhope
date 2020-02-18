@y.package
def coreutils0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/coreutils/coreutils-{version}.tar.xz" 1
             export FORCE_UNSAFE_CONFIGURE=1
             export CFLAGS="$OPENSSL_INCLUDES $CFLAGS $LDFLAGS $LIBS"  
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --libexecdir=$IDIR/bin --without-gmp --enable-single-binary=symlinks --enable-no-install-program=stdbuf || exit 1
             $YMAKE -j $NTHRS || true
             echo >> src/libstdbuf.c
             echo >> 'int main() {}' >> src/libstdbuf.c
             $YMAKE -j $NTHRS
             $YMAKE install

             cd "$IDIR/bin/"
             progs=$(./coreutils --help | tr '\\n' ' ' | sed -e 's/.*\[//' | sed -e 's/ Use: .*//')

             for i in $progs; do
                 ln -fs coreutils $i
             done
        """,
        'version': '8.31',
        'meta': {
            'kind': ['tool', 'box'],
            'depends': ['iconv', 'intl', 'openssl', 'make', 'c'],
            'provides': [
                {'env': 'COREUTILS', 'value': '{pkgroot}/bin/coreutils'},
            ],
        },
    }
