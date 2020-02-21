@y.package
def strace0():
    return {
        'code': '''
            export CPP="$CC -E"
            source fetch "https://github.com/strace/strace/releases/download/v5.5/strace-5.5.tar.xz" 1
            $YSHELL ./configure --prefix=$IDIR --disable-shared --enable-static
            $YMAKE -j $NTHR
            $YMAKE install
        ''',
        'meta': {
            'kind': ['tool'],
            'depends': ['kernel-h', 'make', 'c'],
        },
    }
