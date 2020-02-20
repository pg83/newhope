@y.package
def ninja0():
    return {
        'code': """
             source fetch "https://github.com/ninja-build/ninja/archive/v{version}.tar.gz" 0
             mv ninja* xxx
             cd xxx
             export CFLAGS="-D_BSD_SOURCE=1 $CFLAGS"
             export CXXFLAGS="-D_BSD_SOURCE=1 $CXXFLAGS"
             export LDFLAGS="$LDFLAGS $LIBS"
             $PYTHON ./configure.py --bootstrap
             mkdir -p $IDIR/bin
             install -v -m755 ninja $IDIR/bin
             $YUPX $IDIR/bin/ninja
        """,
        'meta': {
            'kind': ['tool'],
            'depends': ['python', 'c++', 'make', 'c', 'upx'],
            'provides': [
                {'env': 'YNINJA', 'value': '{pkgroot}/bin/ninja'},
                {'env': 'NINJA', 'value': '{pkgroot}/bin/ninja'},
            ],
        },
    }
