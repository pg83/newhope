run_upm = '''#!/bin/sh
exec /bin/upm cmd scheduler CRON
'''


@y.package
def upm0():
    return {
        'code': '''
             source fetch "https://github.com/pg83/newhope/archive/{version}.zip" 0
             (mv newhope* xxx && mv xxx/* ./)
             mkdir $IDIR/bin
             $PYTHON3 ./cli release > upm
             $(F_0)
             $(F_1)
             $YSHELL ./freeze.sh "$PYTHON3" ./upm -w

             $YUPX -o $IDIR/bin/upm upm

             cd $IDIR
             $(F_2)
             chmod +x run
        ''',
        'install': '''#!/bin/sh
            ln -sf ../pkg/$1/bin/upm ../../bin/
            ln -sf ../../pkg/$1 ../../etc/runit/
            rm -rf ./log
        ''',
        'meta': {
            'depends': ['python3', 'upx', 'make', 'c'],
        },
        'extra': [
            {'kind': 'file', 'path': 'freeze.sh', 'data': y.builtin_data('data/freeze.sh')},
            {'kind': 'file', 'path': 'find_modules.py', 'data': y.builtin_data('data/find_modules.py')},
            {'kind': 'file', 'path': 'run', 'data': run_upm},
        ],
    }
