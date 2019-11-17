@y.ygenerator(tier=1)
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
            'kind': ['box'],
            'depends': ['python_pth']
        },
    }
