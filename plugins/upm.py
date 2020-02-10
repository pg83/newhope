@y.package
def upm0():
    return {
        'code': """
             source fetch "https://github.com/pg83/newhope/archive/{version}.zip" 0
             (mv newhope* xxx && mv xxx/* ./)
             mkdir $IDIR/bin
             $PYTHON3 ./cli release  > upm
             $(APPLY_EXTRA_PLAN_0)
             $(APPLY_EXTRA_PLAN_1)
             $YSHELL ./freeze.sh $PYTHON3 ./upm 
             mv upm $IDIR/bin/ && chmod +x $IDIR/bin/upm
        """,
        'version': '7695567dd35b688fc5f435045f7d6a7044db82c9',
        'meta': {
            'kind': ['tool'],
            'depends': ['python3'],
        },
        'extra': [
            {'kind': 'file', 'path': 'freeze.sh', 'data': y.builtin_data('data/freeze.sh')},
            {'kind': 'file', 'path': 'find_modules.py', 'data': y.builtin_data('data/find_modules.py')},
        ],
    }
