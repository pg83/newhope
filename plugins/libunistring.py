@ygenerator(tier=-2, kind=['core', 'library'])
def libunistring0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/libunistring/libunistring-0.9.10.tar.xz" 1
             $YSHELL ./configure --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '0.9.10',
        'meta': {
            'depends': [],
            'provides': [
                {'lib': 'unistring', 'configure': {'opt': '--with-libunistring-prefix={pkg_root}'}},
            ],
        },
    }
