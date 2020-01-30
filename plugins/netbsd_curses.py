@y.package
def netbsd_curses0():
    return {
        'code': """
            source fetch "https://github.com/sabotage-linux/netbsd-curses/archive/{version}.zip" 0
            cd netbsd*
            $YMAKE -j 1 CC="$CC" AR="$AR" RANLIB="$RANLIB" CFLAGS="$CFLAGS $LDFLAGS $LIBS"  LDFLAGS="$LDFLAGS $LIBS" LDFLAGS_HOST="$LDFLAGS $LIBS" PREFIX=/ DESTDIR="$IDIR" all-static install-static
        """,
        'version': '5b0d21692c6c2db31e960961f7a846429e701c30',
        'meta': {
            'kind': ['library'],
            'depends': ['make'],
            'provides': [
                {'lib': 'curses', 'configure': {'opts': ['--with-curses={pkgroot}', '--with-ncurses={pkgroot}']}},
                {'env': 'LIBS', 'value': '"$LIBS -lform -lmenu -lpanel -lcurses -lterminfo"'},
            ],
        },
    }
