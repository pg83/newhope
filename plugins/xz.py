@y.package
def xz0():
    return {
        'code': """
             source fetch "https://sourceforge.net/projects/lzmautils/files/xz-{version}.tar.gz/download" 1
             export CFLAGS="$CFLAGS $LDFLAGS $LIBS"
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static --disable-threads && $YMAKE -j $NTHRS && $YMAKE install
        """,
        'version': '5.2.4',
        'meta': {
            'kind': ['library', 'tool'],
            'depends': ['make', 'c'],
            'provides': [
                {'lib': 'lzma'},
                {'env': 'YXZ', 'value': '{pkgroot}/bin/xz'},
                {'env': 'YXZCAT', 'value': '{pkgroot}/bin/xzcat'},
            ],
        },
    }
