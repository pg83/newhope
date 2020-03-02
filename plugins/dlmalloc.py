@y.package
def dlmalloc0():
    return {
        'code': '''
            source fetch "https://raw.githubusercontent.com/ennorehling/dlmalloc/master/malloc.c" 0
            $CC -DUSE_MALLOC_LOCK=1 -c ./malloc.c -o malloc.o
            $AR q libdlmalloc.a malloc.o
            $RANLIB libdlmalloc.a
            mkdir $IDIR/lib
            cp libdlmalloc.a $IDIR/lib
        ''',
        'meta': {
            'kind': ['library'],
            'contains': ['mimalloc'],
            'depends': ['c'],
            'provides': [
                {'lib': 'dlmalloc'},
            ],
        }
    }
