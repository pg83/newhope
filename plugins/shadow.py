@y.package
def shadow0():
    return {
        'code': '''
             source fetch "https://github.com/shadow-maint/shadow/releases/download/{version}/shadow-{version}.tar.xz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
             ($YUPX $IDIR/bin/*) || true
             ($YUPX $IDIR/sbin/*) || true
        ''',
        'meta': {
            'kind': ['tool'],
            'depends': ['upx', 'intl', 'iconv', 'make', 'c'],
        }
    }
