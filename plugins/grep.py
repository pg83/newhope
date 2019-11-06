@ygenerator(tier=0, kind=['core', 'box', 'tool'])
def grep0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/grep/grep-3.3.tar.xz" 1
             $YSHELL ./configure --prefix=$IDIR || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '3.3',
        'meta': {
            'depends': ['intl', 'libsigsegv', 'iconv']
        },
    }
