@y.ygenerator(tier=-1, kind=['library'])
def pth0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/pth/pth-2.0.7.tar.gz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-optimize --disable-shared --enable-static || exit 1
             $YMAKE 
             $YMAKE install
        """,
        'version': '1.10',
        'meta': {
            'depends': [],
            'provides': [
                {'lib': 'pth', 'configure': {'opts': ['--with-libpth-prefix={pkgroot}', '--with-pth']}},
            ],
        },
    }
