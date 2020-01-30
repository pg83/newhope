@y.package
def pth0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/pth/pth-{version}.tar.gz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-optimize --disable-shared --enable-static || exit 1
             $YMAKE 
             $YMAKE install
        """,
        'version': '2.0.7',
        'meta': {
            'kind': ['library'],
            'depends': [],
            'provides': [
                {'lib': 'pth', 'configure': {'opts': ['--with-libpth-prefix={pkgroot}', '--with-pth']}},
            ],
        },
    }
