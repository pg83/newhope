if '{os}' == 'linux':
    @y.package
    def musl0():
        return {
            'code': """
                cp -pR $MUSL_ROOT/lib $IDIR/
                cp -pR $MUSL_ROOT/include $IDIR/
                rm $IDIR/lib/libmuslalloc.a
            """,
            'meta': {
                'contains': ['musl-boot'],
                'depends': ['busybox-boot', 'mimalloc', 'musl-base'],
                'provides': [
                    {'lib': 'muslc'},
                    {'env': 'CFLAGS', 'value': '"-ffreestanding -w $CFLAGS"'},
                ],
                'repacks': {},
            },
        }

