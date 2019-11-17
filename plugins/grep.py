@y.ygenerator(tier=0)
def grep0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/grep/grep-{version}.tar.xz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '3.3',
        'meta': {
            'kind': ['box'],
            'depends': ['intl', 'libsigsegv', 'iconv']
        },
    }
