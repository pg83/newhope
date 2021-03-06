@y.package
def termcap0():
    return {
        'code': """
            source fetch "https://ftp.gnu.org/gnu/termcap/termcap-{version}.tar.gz" 1
            source fake_binutils
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static 
            $YMAKE -j $NTHRS
            $YMAKE install
        """,
        'meta': {
            'depends': ['make', 'c'],
            'provides': [
                {'lib': 'termcap'},
            ],
        },
    }
