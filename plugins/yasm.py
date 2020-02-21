@y.package
def yasm0():
    return {
        'code': """
               source fetch "http://www.tortall.net/projects/yasm/releases/yasm-{version}.tar.gz" 1
               export LIBS="$LDFLAGS $LIBS"
               export CC_FOR_BUILD="$CC"
               export CFLAGS_FOR_BUILD="$CFLAGS"
               $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared
               $YMAKE DEFAULT_INCLUDES="-I. $CFLAGS" -j $NTHR
               $YMAKE install
        """,
        'meta': {
            'kind': ['box', 'tool'],
            'depends': ['make', 'c'],
        },
    }
