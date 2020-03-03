@y.package
def psmisc0():
    return {
        'code': """
             source fetch "https://downloads.sourceforge.net/project/psmisc/psmisc/psmisc-{version}.tar.xz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static || exit 1
             $(F_0)
             source  subst_string Makefile psmisc1.patch
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'extra': [
            {'kind': 'file', 'path': 'psmisc1.patch', 'data': y.builtin_data('data/psmisc1.patch')},
        ],
        'meta': {
            'depends': ['kernel-h', 'ncurses', 'make', 'c'],
        },
    }
