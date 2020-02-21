@y.package
def openssh_client0():
    return {
        'code': '''
             pp=$(dirname $SSHD)
             p=$(dirname $pp)
             cp -pR $p/bin $IDIR/
        ''',
        'meta': {
            'kind': ['tool'],
            'depends': ['openssh'],
        }
    }
