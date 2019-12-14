@y.ygenerator()
def yasm0():
    return {
        'code': """
               source fetch "http://www.tortall.net/projects/yasm/releases/yasm-{version}.tar.gz" 1
               export LIBS="$LDFLAGS $LIBS"
               $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared
               $YMAKE -j2
               $YMAKE install
        """,
        'version': '1.3.0',
        'meta': {
            'kind': ['box', 'tool'],
        },
    }
