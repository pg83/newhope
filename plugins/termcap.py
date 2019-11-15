@y.ygenerator(tier=1, kind=['library'])
def termcap0():
    return {
        'code': """
            source fetch "https://ftp.gnu.org/gnu/termcap/termcap-1.3.1.tar.gz" 1
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static 
            $YMAKE -j2
            $YMAKE install
        """,
        'version': '1.3.1',
        'meta': {
            'provides': [
                {'lib': 'termcap'},
            ],
        },
    }
