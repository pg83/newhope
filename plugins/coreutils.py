def coreutils_impl(deps, kind):
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/coreutils/coreutils-{version}.tar.xz" 1 
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --libexecdir=$IDIR/bin --without-gmp || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '8.31',
        'meta': {
            'kind': ['tool'] + kind,
            'depends': ['iconv', 'intl'] + deps,
        },
    }


@y.ygenerator()
def coreutils0():
    return coreutils_impl(['openssl'], ['box'])


@y.ygenerator()
def coreutils_boot0():
    return coreutils_impl([], [])
