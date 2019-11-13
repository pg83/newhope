@y.ygenerator(tier=-2, kind=['core', 'library'])
def libsigsegv0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/libsigsegv/libsigsegv-2.12.tar.gz" 1
             $YSHELL ./configure --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '2.12',
        'meta': {
            'depends': [],
            'provides': [
                {'lib': 'libsigsegv', 'configure': {'opt': '--with-libsigsegv-prefix={pkg_root}'}},
            ],
        },
    }
