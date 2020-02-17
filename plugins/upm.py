@y.package
def upm0():
    return {
        'code': """
             source fetch "https://github.com/pg83/newhope/archive/{version}.zip" 0
             (mv newhope* xxx && mv xxx/* ./)
             mkdir $IDIR/bin
             $PYTHON3 ./cli release > upm
             $(APPLY_EXTRA_PLAN_0)
             $(APPLY_EXTRA_PLAN_1)
             $YSHELL ./freeze.sh "$PYTHON3" ./upm -w
             mv upm $IDIR/bin/ && chmod +x $IDIR/bin/upm
        """,
        'version': '2975ad2d75f8a54708048ba59e19aeadb1f83837',
        'meta': {
            'kind': ['tool'],
            'depends': ['python3', 'make', 'c'],
        },
        'extra': [
            {'kind': 'file', 'path': 'freeze.sh', 'data': y.builtin_data('data/freeze.sh')},
            {'kind': 'file', 'path': 'find_modules.py', 'data': y.builtin_data('data/find_modules.py')},
        ],
    }
