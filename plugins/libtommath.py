@y.package
def libtommath0():
    return {
        'code': '''
            source fetch "https://github.com/libtom/libtommath/releases/download/v{version}/ltm-{version}.tar.xz" 0
            (mv libtommath* xxx && mv xxx/* ./)
            $YMAKE -j $NTHRS
            $YMAKE DESTDIR=$IDIR LIBPATH=/lib INCPATH=/include install
        ''',
        'meta': {
            'depends': ['crt', 'make', 'c'],
            'provides': [
                {'lib': 'tommath'},
            ],
        }
    }
