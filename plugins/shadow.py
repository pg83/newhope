#@y.package
def shadow0():
    return {
        'code': '''
             source fetch "https://github.com/shadow-maint/shadow/releases/download/{version}/shadow-{version}.tar.xz" 1
             #(mv shadow* xxx && mv xxx/* ./)
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared || exit 1
             $YMAKE -j $THRS
             $YMAKE install
             #($YUPX $IDIR/bin/*) || true
        ''',
        'version': '4.8.1',
        'meta': {
            'kind': ['tool'],
            'depends': ['intl', 'iconv', 'make', 'c'],
        }
    }
