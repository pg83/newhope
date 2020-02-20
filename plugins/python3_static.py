@y.package
def python3_static0():
    return {
        'code': """
            $(APPLY_EXTRA_PLAN_0)
            $(APPLY_EXTRA_PLAN_1)
            $(APPLY_EXTRA_PLAN_2)

            $YSHELL ./freeze_python.sh $PYTHON3
            mkdir $IDIR/bin
            $YUPX -o $IDIR/bin/staticpython3 staticpython
        """,
        'extra': [
            {'kind': 'file', 'path': 'freeze.sh', 'data': y.builtin_data('data/freeze.sh')},
            {'kind': 'file', 'path': 'freeze_python.sh', 'data': y.builtin_data('data/freeze_python.sh')},
            {'kind': 'file', 'path': 'find_modules.py', 'data': y.builtin_data('data/find_modules.py')},
        ],
        'meta': {
            'kind': ['tool'],
            'depends': ['python3', 'upx', 'make', 'c'],
            'provides': [
                {'lib': 'python3.8'},
                {'env': 'STATICPYTHON3', 'value': '{pkgroot}/bin/staticpython3'},
            ],
        },
    }
