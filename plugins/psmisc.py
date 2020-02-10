@y.package
def psmisc0():
    return {
        'code': """
             source fetch "https://downloads.sourceforge.net/project/psmisc/psmisc/psmisc-{version}.tar.xz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'version': '23.3',
        'meta': {
            'kind': ['tool'],
            'depends': ['kernel-h', 'ncurses'],
        },
    }
