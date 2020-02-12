@y.package
def psmisc0():
    return {
        'code': """
             source fetch "https://downloads.sourceforge.net/project/psmisc/psmisc/psmisc-{version}.tar.xz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static || exit 1
             $(APPLY_EXTRA_PLAN_0)
             source  subst_string Makefile psmisc1.patch
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'version': '23.3',
        'extra': [
            {'kind': 'file', 'path': 'psmisc1.patch', 'data': y.builtin_data('data/psmisc1.patch')},
        ],
        'meta': {
            'kind': ['tool'],
            'depends': ['kernel-h', 'ncurses'],
        },
    }
