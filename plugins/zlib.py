@y.ygenerator(tier=-1, kind=['core', 'dev', 'library'])
def zlib0():
    return {
        'code': """
            source fetch "http://zlib.net/zlib-1.2.11.tar.gz" 1
            $YSHELL ./configure --static --64 --prefix=$IDIR || exit 1
            $YMAKE -j2 && $YMAKE install
        """,
        'version': '1.2.11',
        'meta': {
            'depends': [],
            'provides': [
                {'lib': 'zlib', 'configure': {'opt': '--with-z={pkg_path}'}},
            ],
        },
    }
