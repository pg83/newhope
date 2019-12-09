@y.ygenerator()
def xz0():
    return {
        'code': """
             source fetch "https://sourceforge.net/projects/lzmautils/files/xz-{version}.tar.gz/download" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static && $YMAKE -j2 && $YMAKE install
        """,
        'version': '5.2.4',
        'meta': {
            'kind': ['compression', 'library', 'tool'],
            'provides': [
                {'lib': 'lzma'},
                {'env': 'YXZ', 'value': '{pkgroot}/bin/xz'},
                {'env': 'YXZCAT', 'value': '{pkgroot}/bin/xzcat'},
            ],
        },
    }
