@y.package
def strace0():
    return {
        'code': '''
            echo '#!/bin/sh' > gcc
            echo "$CC $CFLAGS \"\$@\"" >> gcc

            echo '#!/bin/sh' > cpp
            echo "$CC -E $CFLAGS \"\$@\"" >> cpp

            chmod +x gcc
            chmod +x cpp

            export PATH="$(pwd):$PATH"
            source fetch "https://github.com/strace/strace/releases/download/v{version}/strace-{version}.tar.xz" 1
            $YSHELL ./configure  --prefix=$IDIR --disable-shared --enable-static --enable-mpers=no
            $YMAKE CFLAGS_FOR_BUILD="$CFLAGS" -j $NTHR
            $YMAKE install
        ''',
        'meta': {
            'depends': ['kernel-h', 'make', 'c'],
        },
    }
