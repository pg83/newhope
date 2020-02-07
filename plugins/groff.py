@y.package
def groff0():
    return {
        'code': """
             source fetch "http://ftp.gnu.org/gnu/groff/groff-{version}.tar.gz" 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'version': '1.22.4',
        'meta': {
            'kind': ['tool'],
            'depends': [
            ],
            'provides': [
                {'env': 'GROFF', 'value': '{pkgroot}/bin/groff'},
            ],
        }
    }
