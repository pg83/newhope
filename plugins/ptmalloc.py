@y.package
def ptmalloc30():
    return {
        'code': ''' 
            source fetch "http://www.malloc.de/malloc/ptmalloc3-current.tar.gz" 0
            mv ptmalloc* xxx
            mv xxx/* ./
            $YMAKE CC="$CC" AR="$AR" RANLIB="$RANLIB" OPT_CFLAGS="$CFLAGS" libptmalloc3.a
            mkdir $IDIR/lib
            mv libptmalloc3.a $IDIR/lib/
        ''',
        'meta': {
            'kind': ['library'],
            'depends': ['make', 'c'],
            'contains': ['mimalloc'],
            'provides': [
                {'lib': 'ptmalloc3'},
            ],
        },
    }
