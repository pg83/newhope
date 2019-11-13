@y.ygenerator(tier=0, kind=['core', 'box', 'tool'])
def curl0():
    return {
        'code': """
            source fetch "https://curl.haxx.se/snapshots/curl-7.67.0-20191011.tar.bz2" 1
            $YSHELL ./configure --prefix=$IDIR --enable-static --disable-shared
            $YMAKE -j2
            $YMAKE install
        """,
        'version': '7.67.0',
        'meta': {
            'depends': ['mbedtls', 'libidn2'],
            'configure': [
                {'opt': '--with-secure-transport', 'os': 'darwin'},
            ]
        },
    }
