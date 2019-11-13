@y.ygenerator(tier=-2, kind=['core', 'library'])
def libedit0():
    return {
        'code': """
             source fetch "https://www.thrysoee.dk/editline/libedit-20191025-3.1.tar.gz" 1
             $YSHELL ./configure --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '20191025-3.1',
        'meta': {
            'depends': [],
            'provides': [
                {'lib': 'libedit'},
            ],
        },
    }
