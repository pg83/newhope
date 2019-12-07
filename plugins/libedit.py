@y.ygenerator()
def libedit0():
    return {
        'code': """
             source fetch "http://thrysoee.dk/editline/libedit-{version}.tar.gz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '20191025-3.1',
        'meta': {
            'kind': ['library'],
            'depends': [],
            'provides': [
                {'lib': 'edit'},
            ],
        },
    }
