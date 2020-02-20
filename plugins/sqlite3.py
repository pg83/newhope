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
            'kind': ['library', 'tool'],
            'depends': ['readline', 'make', 'c'],
            'provides': [
                {'lib': 'sqlite3'},
            ],
        },
    }
