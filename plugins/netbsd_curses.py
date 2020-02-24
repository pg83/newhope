@y.package
def netbsd_curses0():
    return {
        'code': """
            source fetch "https://github.com/sabotage-linux/netbsd-curses/archive/{version}.zip" 0
            cd netbsd*
            $YMAKE -j 1 CC="$CC" AR="$AR" RANLIB="$RANLIB" CFLAGS="$CFLAGS $LDFLAGS $LIBS"  LDFLAGS="$LDFLAGS $LIBS" LDFLAGS_HOST="$LDFLAGS $LIBS" PREFIX=/ DESTDIR="$IDIR" all-static install-static
        """,
        'meta': {
            'kind': ['library'],
            'depends': ['make', 'c'],
            'provides': [
                {'lib': 'curses'},
                {'configure': '--with-curses={pkgroot}'},
                {'configure': '--with-ncurses={pkgroot}'},
                {'env': 'LIBS', 'value': '"$LIBS -lform -lmenu -lpanel -lcurses -lterminfo"'},
                {'env': 'NCURSES_CFLAGS', 'value': '"-I{pkgroot}/include"'},
                {'env': 'NCURSESW_CFLAGS', 'value': '"-I{pkgroot}/include"'},
                {'env': 'NCURSES_LIBS', 'value': '"-lform -lmenu -lpanel -lcurses -lterminfo"'},
                {'env': 'NCURSESW_LIBS', 'value': '"-lform -lmenu -lpanel -lcurses -lterminfo"'},
            ],
        },
    }
