@y.package
def libarchive0():
    return {
        'code': """
             source fetch "https://libarchive.org/downloads/libarchive-{version}.tar.gz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'version': '3.4.0',
        'meta': {
            'kind': ['library', 'tool', 'box'],
            'depends': ['zlib-dev', 'bzip2-dev', 'xz-dev', 'make', 'c'],
            'provides': [
                {'lib': 'archive'},
                {'env': 'YTAR', 'value': '{pkgroot}/bin/bsdtar'},
                {'env': 'YBSDTAR', 'value': '{pkgroot}/bin/bsdtar'},
            ],
        },
    }
