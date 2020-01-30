@y.package
def xz0():
    return {
        'code': """
             source fetch "https://sourceforge.net/projects/lzmautils/files/xz-{version}.tar.gz/download" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static --disable-threads && $YMAKE -j $NTHRS && $YMAKE install
        """,
        'version': '5.2.4',
        'meta': {
            'kind': ['box', 'library', 'tool'],
            'provides': [
                {'lib': 'lzma'},
                {'env': 'YXZ', 'value': '{pkgroot}/bin/xz'},
                {'env': 'YXZCAT', 'value': '{pkgroot}/bin/xzcat'},
            ],
        },
    }
