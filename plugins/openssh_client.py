keygen_sh='''
touch $HOME/.ssh_agent
. $HOME/.ssh_agent
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
             $(F_0)
             $(F_1)
             chmod +x run
        ''',
        'install': '''
            ln -sf ../../pkg/$1 ../../etc/runit/
            ln -sf ../../pkg/$1/03-keygen.sh ../../etc/profile.d/
            rm -rf ./log
        ''',
        'meta': {
            'depends': ['openssh', 'upx'],
            'repacks': {},
        },
        'extra': [
            {'kind': 'file', 'path': 'run', 'data': y.builtin_data('data/ssh_agent_run.py')},
            {'kind': 'file', 'path': '03-keygen.sh', 'data': keygen_sh},
        ],
    }
