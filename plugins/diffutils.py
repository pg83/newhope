@y.ygenerator()
def diffutils0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/diffutils/diffutils-{version}.tar.xz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-gcc-warnings || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'version': '3.7',
        'meta': {
            'kind': ['box', 'tool'],
            'depends': ['iconv', 'intl', 'libsigsegv']
        },
    }
