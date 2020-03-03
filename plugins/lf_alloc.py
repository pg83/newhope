@y.package
def lf_alloc0():
    return {
        'code': '''
            source fetch "https://github.com/pg83/lf_alloc/archive/788773952016f166183c11e7b25e98c01bd06ada.zip" 0
            (mv lf* xxx && mv xxx/* ./)
            $YMAKE CC="$CC" AR="$AR" RANLIB="$RANLIB" CFLAGS="$CFLAGS"
            mkdir $IDIR/lib
            mv liblfalloc.a $IDIR/lib/
        ''',
        'meta': {
            'kind': ['library'],
            'depends': ['make', 'c', 'c++'],
            'contains': ['mimalloc'],
            'provides': [
                {'lib': 'lfalloc'},
            ],
        },
    }
