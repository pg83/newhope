@y.package
def dash0():
    return {
        'code': '''
            source fetch "http://gondor.apana.org.au/~herbert/dash/files/dash-{version}.tar.gz" 1
            export CFLAGS_FOR_BUILD="$CFLAGS $LDFLAGS $LIBS"
            $YSHELL ./configure $COFLAGS --prefix=$IDIR
            $YMAKE -j $NTHRS
            $YMAKE install
        ''',
        'install': '''
            ln -sf ../pkg/$1/bin/dash ../../bin/sh
        ''',
        'meta': {
            'depends': ['libedit', 'make', 'c'],
            'provides': [
                {'tool': 'YSHELL', 'value': '{pkgroot}/bin/dash'},
                {'tool': 'DASH', 'value': '{pkgroot}/bin/dash'},
            ],
        },
    }
