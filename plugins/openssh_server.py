@y.package
def openssh_server0():
    return {
        'code': '''
             pp=$(dirname $SSHD)
             p=$(dirname $pp)
             cp -pR $p/sbin $IDIR/bin
        ''',
        'meta': {
            'kind': ['tool'],
            'depends': ['openssh'],
            'provides': [
                {'env': 'SSHD', 'value': '{pkgroot}/bin/sshd'}
            ],
        }
    }
