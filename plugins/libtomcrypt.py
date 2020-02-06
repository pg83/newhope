@y.package
def libtomcrypt0():
    return {
        'code': '''
            source fetch "https://github.com/libtom/libtomcrypt/releases/download/v{version}/crypt-{version}.tar.xz" 1
            $YMAKE -j $THRS
            $YMAKE DESTDIR=$IDIR install
        ''',
        'version': '1.18.2',
        'meta': {
            'kind': ['library'],
            'depends': ['libtommath'],
            'provides': [
                {'lib': 'tommath'},
            ],
        }
    }
