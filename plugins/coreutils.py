@y.ygenerator(tier=0, kind=['box'])
def coreutils0():
    version = '8.31'

    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/coreutils/coreutils-{version}.tar.xz" 1 
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --without-gmp || exit 1
             $YMAKE -j2
             $YMAKE install
        """.format(version=version),
        'version': version,
        'meta': {
            'depends': ['iconv', 'intl', 'pth'],
            'soft': ['openssl'],
        },
    }
