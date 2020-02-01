@y.package
def coreutils0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/coreutils/coreutils-{version}.tar.xz" 1
             export FORCE_UNSAFE_CONFIGURE=1 
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --libexecdir=$IDIR/bin --without-gmp --enable-single-binary=symlinks --enable-no-install-program=stdbuf || exit 1
             $YMAKE -j $NTHRS || true
             echo >> src/libstdbuf.c
             echo >> 'int main() {}' >> src/libstdbuf.c
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'version': '8.31',
        'meta': {
            'kind': ['tool', 'box'],
            'depends': ['iconv', 'intl', 'openssl'],
            'provides': [
                {'env': 'COREUTILS', 'value': '{pkgroot}/bin/coreutils'},
            ],
        },
    }
