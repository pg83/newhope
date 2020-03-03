@y.package
def mimalloc0():
    depends = []

    if '{os}' == 'linux':
        depends = ['musl-boot', 'kernel-h']

    return {
        'code': """
             source fetch "https://github.com/microsoft/mimalloc/archive/{version}.zip" 0
             (mv mim* xxx && mv xxx/* ./)
             $CC $CFLAGS -DMI_MALLOC_OVERRIDE=1 -DMI_DEBUG=0 -std=c11 -Iinclude -Dasm=__asm__ -c src/static.c -o static.o
             $AR q libmimalloc.a static.o
             $RANLIB libmimalloc.a
             mkdir $IDIR/lib
             mv libmimalloc.a $IDIR/lib/ 
        """,
        'meta': {
            'depends': depends + ['make-boot'],
            'provides': [
                {'lib': 'mimalloc'},
            ],
        },
    }
