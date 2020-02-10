@y.package
def mimalloc0():
    depends = []

    if '{os}' == 'linux':
        depends = ['musl-boot', 'kernel-h']

    return {
        'code': """
             source fetch "https://github.com/microsoft/mimalloc/archive/{version}.zip" 0
             (mv mim* xxx && mv xxx/* ./)
             $CC $CFLAGS -DMI_MALLOC_OVERRIDE=1 -std=c11 -Iinclude -Dasm=__asm__ -c src/static.c -o static.o
             $AR q libmimalloc.a static.o
             $RANLIB libmimalloc.a
             mkdir $IDIR/lib
             mv libmimalloc.a $IDIR/lib/ 
        """,
        'version': '6a744a8549263696ef8d620006a0de2249e59b46',
        'meta': {
            'kind': ['library'],
            'depends': depends + ['make-boot'],
            'undeps': ['make', 'musl'],
            'provides': [
                {'lib': 'mimalloc'},
            ],
        },
    }
