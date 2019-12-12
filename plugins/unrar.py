@y.ygenerator()
def unrar0():
    return {
        'code': """
             CXX=$(which clang++)
             source fetch "http://www.rarlab.com/rar/unrarsrc-{version}.tar.gz" 0
             cd unrar
             echo $CXX
             (echo "CXX=$CXX"; cat makefile) | grep -v 'CXX=c++' > mk1; mv mk1 makefile
             $YMAKE -f makefile
             mkdir -p $IDIR/bin
             install -v -m755 unrar $IDIR/bin
        """,
        'version': '5.8.3',
        'meta': {
            'kind': ['compression', 'tool'],
            'provides': [
                {'env': 'YUNRAR', 'value': '{pkgroot}/bin/unrar'},
            ],
        },
    }
