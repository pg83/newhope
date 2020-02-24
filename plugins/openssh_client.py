keygen_sh='''
touch $HOME/.ssh_agent
. $HOME/.ssh_agent
'''

install_agent = '''
ln -sf ../../pkg/$1 ../../etc/runit/
ln -sf ../../pkg/$1/03-keygen.sh ../../etc/profile.d/
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
             $(F_0)
             $(F_1)
             $(F_2)
             chmod +x run
        ''',
        'meta': {
            'kind': ['tool'],
            'depends': ['openssh', 'upx'],
            'repacks': {},
        },
        'extra': [
            {'kind': 'file', 'path': 'run', 'data': y.builtin_data('data/ssh_agent_run.py')},
            {'kind': 'file', 'path': 'install', 'data': install_agent},
            {'kind': 'file', 'path': '03-keygen.sh', 'data': keygen_sh},
        ],
    }
