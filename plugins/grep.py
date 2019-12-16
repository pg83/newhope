@y.ygenerator()
def grep0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/grep/grep-{version}.tar.xz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'version': '3.3',
        'meta': {
            'kind': ['box', 'tool'],
            'depends': ['intl', 'libsigsegv', 'iconv']
        },
    }
