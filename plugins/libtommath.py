@y.package
def libtommath0():
    return {
        'code': '''
            source fetch "https://github.com/libtom/libtommath/releases/download/v{version}/ltm-{version}.tar.xz" 1
            $YMAKE -j $THRS
            $YMAKE DESTDIR=$IDIR install
        ''',
        'version': '1.2.0',
        'meta': {
            'kind': ['library'],
            'depends': ['compiler_rt'],
            'provides': [
                {'lib': 'tommath'},
            ],
        }
    }
