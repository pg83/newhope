@y.package
def nano0():
    return {
        'code': """
            source fetch "https://www.nano-editor.org/dist/v4/nano-{version}.tar.xz" 1
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared
            $YMAKE -j $NTHRS
            $YMAKE install
        """,
        'meta': {
            'kind': ['tool'],
            'depends': ['intl', 'iconv', 'readline', 'ncurses', 'make', 'c', 'kernel-h'],
        },
    }
