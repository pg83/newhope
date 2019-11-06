@ygenerator(tier=0, kind=['core', 'box', 'tool'])
def coreutils0():
    version = '8.31'

    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/coreutils/coreutils-{version}.tar.xz" 1 
             $YSHELL ./configure --prefix=$IDIR --without-gmp || exit 1
             $YMAKE -j2
             $YMAKE install
        """.format(version=version),
        'version': version,
        'meta': {
            'depends': ['iconv', 'intl', 'pth', 'openssl'],
        },
    }
