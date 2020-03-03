@y.package
def sqlite30():
    return {
        'code': """
            source fetch "https://www.sqlite.org/2019/sqlite-autoconf-{version}.tar.gz" 1
            export CFLAGS="-DSQLITE_OMIT_LOAD_EXTENSION=1 $CFLAGS"
            $YSHELL ./configure $COFLAGS --disable-shared --enable-static  --prefix=$IDIR || exit 1
            $YMAKE install || exit 1
        """,
        'meta': {
            'depends': ['readline', 'make', 'c'],
            'provides': [
                {'lib': 'sqlite3'},
                {'configure': '--with-sqlite3="{pkgroot}"'},
                {'tool': 'SQLITE3_TOOL', 'value': '"{pkgroot}/bin/sqlite3"'},
                {'env': 'SQLITE3_ROOT', 'value': '"{pkgroot}"'}
            ],
        },
    }
