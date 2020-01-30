#if defined(__LINUX__)
    def musl_boot0():
        return {
            'code': code,
            'version': '1.1.24', 
            'extra': [
                {'kind': 'file', 'path': 'mk.sh', 'data': y.globals.by_name['data/mk_musl.sh']['data']},
                {'kind': 'file', 'path': 'crt/dso.c', 'data': y.globals.by_name['data/dso.c']['data']},
                {'kind': 'file', 'path': 'malloc.sh', 'data': y.globals.by_name['data/malloc.sh']['data']},
            ],
            'meta': {
                'kind': ['tool'],
                'depends': ['bestbox'],
                'provides': [
                    {'lib': 'muslc'},
                    {'env': 'CPPFLAGS', 'value': '"$CPPFLAGS -I{pkgroot}/include"'},
                    {'env': 'CFLAGS', 'value': '"-w $CFLAGS"'},
                ],
            },
        }
#endif
