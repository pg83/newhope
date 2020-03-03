@y.package
def xz0():
    return {
        'code': """
             source fetch "https://sourceforge.net/projects/lzmautils/files/xz-{version}.tar.gz/download" 1
             export CFLAGS="$CFLAGS $LDFLAGS $LIBS"
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static --disable-threads && $YMAKE -j $NTHRS && $YMAKE install
        """,
        'meta': {
            'depends': ['make', 'c'],
            'provides': [
                {'lib': 'lzma'},
                {'tool': 'YXZ', 'value': '{pkgroot}/bin/xz'},
                {'tool': 'YXZCAT', 'value': '{pkgroot}/bin/xzcat'},
                {'configure': '--with-lzma={pkgroot}'},
            ],
        },
    }
