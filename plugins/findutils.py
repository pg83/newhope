@y.package
def findutils0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/pub/gnu/findutils/findutils-{version}.tar.xz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'meta': {
            'depends': ['python', 'intl', 'iconv'],
        },
    }
