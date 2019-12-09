@y.ygenerator()
def musl0():
    return {
        'os': 'linux',
        'code': """
            source fetch "https://www.musl-libc.org/releases/musl-{version}.tar.gz" 1
            $YSHELL ./configure --prefix=$IDIR --enable-static --disable-shared || exit 1
            $YMAKE -j3 || exit 1 
            $YMAKE install || exit 2
        """,
        'version': '1.1.24', 
        'meta': {
            'kind': ['library'],
            'depends': ['bestbox'],
            'provides': [
                {'lib': 'c'},
                {'env': 'CFLAGS', 'value': '"-nostdinc -nostdlib $CFLAGS"'},
            ],
        },
    }
