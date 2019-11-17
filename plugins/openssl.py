@y.ygenerator(tier=3)
def openssl0():
    version = '1.1.1c'

    return {
        'code': """
            source fetch "https://www.openssl.org/source/old/{minver}/openssl-{version}.tar.gz" 1
            $YSHELL ./configure $COFLAGS --prefix=$IDIR
            $YMAKE -j2
            $YMAKE install
        """.replace('{minver}', version[:-1]),
        'version': version,
        'meta': {
            'kind': ['library'],
            'depends': [],
            'provides': [
                {'lib': 'openssl'},
            ],
        },
    }
