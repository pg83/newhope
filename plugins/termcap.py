@y.package
def termcap0():
    return {
        'code': """
            source fetch "https://ftp.gnu.org/gnu/termcap/termcap-{version}.tar.gz" 1
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static 
            $YMAKE -j $NTHRS
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
