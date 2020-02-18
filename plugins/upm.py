install_upm = '''
ln -sf ../pkg/$1/bin/upm ../../bin/
ln -sf ../../pkg/$1 ../../etc/runit/
'''

run_upm = '''
#!/bin/sh
/bin/upm cmd scheduler CRON
'''

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

             cd $IDIR
             $(APPLY_EXTRA_PLAN_2)
             $(APPLY_EXTRA_PLAN_3)
             chmod +x install
             chmod +x run
        """,
        'version': '025850cb557ddf4c4780d0403dde50ff26686ce4',
        'meta': {
            'kind': ['tool'],
            'depends': ['python3', 'make', 'c'],
        },
        'extra': [
            {'kind': 'file', 'path': 'freeze.sh', 'data': y.builtin_data('data/freeze.sh')},
            {'kind': 'file', 'path': 'find_modules.py', 'data': y.builtin_data('data/find_modules.py')},
            {'kind': 'file', 'path': 'install', 'data': install_upm},
            {'kind': 'file', 'path': 'run', 'data': run_upm},
        ],
    }
