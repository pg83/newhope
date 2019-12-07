@y.ygenerator()
def openssl0():
    version = '1.1.1c'

    return {
        'code': """
            source fetch "https://www.openssl.org/source/old/{minver}/openssl-{version}.tar.gz" 1
            $YPERL ./Configure darwin64-x86_64-cc no-shared no-dso no-hw no-engine --prefix=$IDIR --openssldir=$IDIR $CFLAGS $LDFLAGS
            $YMAKE -j2
            $YMAKE install
        """.replace('{minver}', version[:-1]),
        'version': version,
        'meta': {
            'kind': ['library'],
            'depends': [],
            'provides': [
                {'lib': 'ssl'},
            ],
        },
    }
