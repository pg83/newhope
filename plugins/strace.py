@y.package
def strace0():
    return {
        'code': '''
            export CPP="$CC -E"
            ln -s "$CC" ./gcc
            export PATH="$(pwd):$PATH"
            source fetch "https://github.com/strace/strace/releases/download/v{version}/strace-{version}.tar.xz" 1
            $YSHELL ./configure  --prefix=$IDIR --disable-shared --enable-static
            $YMAKE CFLAGS_FOR_BUILD="$CFLAGS" -j $NTHR
            $YMAKE install
        ''',
        'version': '5.5',
        'meta': {
            'kind': ['tool'],
            'depends': ['kernel-h', 'make', 'c'],
        },
    }
