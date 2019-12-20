def coreutils_impl(deps, kind):
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
            'kind': ['tool'] + kind,
            'depends': ['iconv', 'intl'] + deps,
            'provides': [
                {'env': 'COREUTILS', 'value': '{pkgroot}/bin/coreutils'},
            ],
        },
    }


@y.ygenerator()
def coreutils0():
    return coreutils_impl(['openssl'], ['box'])


@y.ygenerator()
def coreutils_boot0():
    return coreutils_impl([], [])
