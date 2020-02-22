install_agent = '''
ln -sf ../../pkg/$1 ../../etc/runit/
rm -rf ./log
'''

@y.package
def openssh_client0():
    return {
        'code': '''
             pp=$(dirname $SSHD)
             p=$(dirname $pp)
             cp -pR $p/bin $IDIR/
             $YUPX $IDIR/bin/*

             cd $IDIR
             $(APPLY_EXTRA_PLAN_0)
             $(APPLY_EXTRA_PLAN_1)
             chmod +x run
        ''',
        'meta': {
            'kind': ['tool'],
            'depends': ['openssh', 'upx'],
        },
        'extra': [
            {'kind': 'file', 'path': 'run', 'data': y.builtin_data('data/ssh_agent_run.py')},
            {'kind': 'file', 'path': 'install', 'data': install_agent},
        ],
    }
