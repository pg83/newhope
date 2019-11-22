@y.ygenerator(tier=1)
def termcap0():
    return {
        'code': """
            source fetch "https://ftp.gnu.org/gnu/termcap/termcap-{version}.tar.gz" 1
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static 
            $YMAKE -j2
            $YMAKE install
        """,
        'version': '1.3.1',
        'meta': {
            'kind': ['library'],
            'provides': [
                {'lib': 'termcap'},
            ],
        },
    }