@y.ygenerator(tier=-2, kind=['core', 'library'])
def libffi0():
    return {
        'code': """
             source fetch "https://sourceware.org/ftp/libffi/libffi-3.2.1.tar.gz" 1
             $YSHELL ./configure --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '3.2.1',
        'meta': {
            'depends': [],
            'provides': [
                {'lib': 'libffi'},
            ],
        },
    }
