if '{os}' == 'linux':
    @y.package
    def musl_alloc0():
        return {
            'code': """
                mkdir $IDIR/lib
                cp -pR $MUSL_ROOT/lib/libmuslalloc.a $IDIR/lib/
            """,
            'meta': {
                'kind': ['library'],
                'contains': ['mimalloc'],
                'depends': ['busybox-boot', 'mimalloc', 'musl-base'],
                'provides': [
                    {'lib': 'muslalloc'},
                ],
                'repacks': {},
            },
        }

