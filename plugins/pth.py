@y.ygenerator(tier=-1, kind=['core', 'library'])
def pth0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/pth/pth-2.0.7.tar.gz" 1
             $YSHELL ./configure --prefix=$IDIR --enable-optimize --disable-shared --enable-static || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '1.10',
        'meta': {
            'depends': [],
            'provides': [
                {'lib': 'pth', 'configure': {'opt': '--with-libpth-prefix={pkg_root}'}}
            ],
        },
    }
