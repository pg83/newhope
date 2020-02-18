@y.package
def dash0():
    return {
        'code': """
            source fetch "http://gondor.apana.org.au/~herbert/dash/files/dash-{version}.tar.gz" 1
            export CFLAGS_FOR_BUILD="$CFLAGS $LDFLAGS $LIBS"
            $YSHELL ./configure $COFLAGS --prefix=$IDIR
            $YMAKE -j $NTHRS
            $YMAKE install

            echo 'ln -sf ../pkg/$1/bin/dash ../../bin/sh' > $IDIR/install && chmod +x $IDIR/install
         """,
        'version': '0.5.10.2',
        'meta': {
            'kind': ['box', 'tool'],
            'depends': ['libedit', 'make', 'c'],
            'provides': [
                {'env': 'YSHELL', 'value': '{pkgroot}/bin/dash'},
                {'env': 'DASH', 'value': '{pkgroot}/bin/dash'},
            ],
        },
    }
