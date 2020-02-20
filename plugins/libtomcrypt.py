@y.package
def libtomcrypt0():
    return {
        'code': '''
            source fetch "https://github.com/libtom/libtomcrypt/releases/download/v{version}/crypt-{version}.tar.xz" 0
            (mv lib* xxx && mv xxx/* ./)
            CFLAGS="$CFLAGS -DUSE_LTM -DLTM_DESC" $YMAKE -j $THRS
            $YMAKE DESTDIR=$IDIR LIBPATH=/lib INCPATH=/include install
        ''',
        'meta': {
            'kind': ['library'],
            'depends': ['libtommath', 'make', 'c'],
            'provides': [
                {'lib': 'tomcrypt'},
                {'env': 'CFLAGS', 'value': '"-DUSE_LTM -DLTM_DESC"'},
            ],
        }
    }
