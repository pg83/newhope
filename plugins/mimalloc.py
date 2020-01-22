@y.ygenerator()
def mimalloc0():
    return {
        'code': """
             source fetch "https://github.com/microsoft/mimalloc/archive/acb03c54971c4b0a43a6d17ea55a9d5feb88972f.zip" 0
             (mv mim* xxx && mv xxx/* ./)
             $CC $CFLAGS -DMI_MALLOC_OVERRIDE=1 -std=c11 -Iinclude -Dasm=__asm__ -c src/static.c -o static.o
             $AR q libmimalloc.a static.o
             $RANLIB libmimalloc.a
             mkdir $IDIR/lib
             mv libmimalloc.a $IDIR/lib/             
        """,
        'version': '',
        'meta': {
            'kind': ['library'],
            'depends': [
                {
                    'os': 'linux',
                    'value': 'musl-boot',
                },
                {
                    'os': 'linux',
                    'value': 'kernel-h'
                },
            ],
            'provides': [
                {'lib': 'mimalloc'},
            ],
        },
    }