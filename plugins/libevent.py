@y.package
def libevent0():
    return {
        'code': '''
            source fetch "https://github.com/libevent/libevent/releases/download/release-{version}/libevent-{version}.tar.gz" 1
            $YSHELL ./configure --prefix=$IDIR --enable-static --disable-shared || exit 1
            $YMAKE -j $NTHRS
            $YMAKE install
        ''',
        'meta': {
            'depends': ['openssl', 'make', 'c'],
            'provides': [
                {'lib': 'event'},
                {'env': 'LIBEVENT_ROOT', 'value': '"{pkgroot}"'},
            ],
        },
    }
