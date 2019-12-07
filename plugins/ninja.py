@y.ygenerator()
def ninja0():
    return {
        'code': """
             source fetch "https://github.com/ninja-build/ninja/archive/v{version}.tar.gz" 1
             $PYTHON ./configure.py --bootstrap
             mkdir -p $IDIR/bin
             install -v -m755 ninja $IDIR/bin
        """,
        'version': '1.9.0',
        'meta': {
            'kind': ['box', 'tool'],
            'depends': ['python-pth'],
            'provides': [
                {'env': 'YNINJA', 'value': '{pkgroot}/bin/ninja'},
            ],
        },
    }
