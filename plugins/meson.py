@y.package
def meson0():
    return {
        'code': """
             source fetch "https://github.com/mesonbuild/meson/releases/download/{version}/meson-{version}.tar.gz" 1
             mkdir $IDIR/bin
             $(APPLY_EXTRA_PLAN_0)
             $(APPLY_EXTRA_PLAN_1)
             $PYTHON3 ./freeze.py ./meson.py . 
             $YMAKE -j $NTHR
             $YUPX -o $IDIR/bin/meson meson
        """,
        'version': '0.53.1',
        'meta': {
            'kind': ['tool'],
            'depends': ['python3', 'upx', 'make', 'c'],
            'provides': [
                {'env': 'MESON', 'value': '{pkgroot}/bin/meson'},
            ],
        },
        'extra': [
            {'kind': 'file', 'path': 'freeze.py', 'data': y.builtin_data('data/freeze.py')},
            {'kind': 'file', 'path': 'find_modules.py', 'data': y.builtin_data('data/find_modules.py')},
        ],
    }
