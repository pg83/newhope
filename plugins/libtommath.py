@y.package
def libtommath0():
    return {
        'code': '''
            source fetch "https://github.com/libtom/libtommath/releases/download/v{version}/ltm-{version}.tar.xz" 0
            (mv libtommath* xxx && mv xxx/* ./)
            $YMAKE -j $THRS
            $YMAKE DESTDIR=$IDIR LIBPATH=/lib INCPATH=/include install
        ''',
        'version': '1.2.0',
        'meta': {
            'kind': ['library'],
            'depends': ['crt', 'make', 'c'],
            'provides': [
                {'lib': 'tommath'},
            ],
        }
    }
