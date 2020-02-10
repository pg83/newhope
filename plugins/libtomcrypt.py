@y.package
def libtomcrypt0():
    return {
        'code': '''
            source fetch "https://github.com/libtom/libtomcrypt/releases/download/v{version}/crypt-{version}.tar.xz" 0
            (mv lib* xxx && mv xxx/* ./)
            $YMAKE -j $THRS
            $YMAKE DESTDIR=$IDIR LIBPATH=/lib INCPATH=/include install
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
