@y.ygenerator(tier=-2, kind=['library'])
def libedit0():
    return {
        'code': """
             source fetch "http://thrysoee.dk/editline/libedit-20191025-3.1.tar.gz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '20191025-3.1',
        'meta': {
            'depends': [],
            'provides': [
                {'lib': 'edit'},
            ],
        },
    }
