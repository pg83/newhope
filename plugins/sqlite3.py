@y.ygenerator()
def sqlite30():
    return {
        'code': """
            source fetch "https://www.sqlite.org/2019/sqlite-autoconf-{version}.tar.gz" 1
            $YSHELL ./configure $COFLAGS --disable-shared --enable-static  --prefix=$IDIR || exit 1
            $YMAKE install || exit 1
        """,
        'version': '3300100',
        'meta': {
            'kind': ['library', 'tool', 'box'],
            'depends': ['readline'],
            'provides': [
                {'lib': 'sqlite3'},
            ],
        },
    }
