@y.package
def libarchive0():
    return {
        'code': """
             source fetch "https://libarchive.org/downloads/libarchive-{version}.tar.gz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'meta': {
            'kind': ['library', 'tool', 'box'],
            'depends': ['zlib', 'bzip2', 'xz', 'make', 'c'],
            'provides': [
                {'lib': 'archive'},
                {'tool': 'YTAR', 'value': '{pkgroot}/bin/bsdtar'},
                {'tool': 'YBSDTAR', 'value': '{pkgroot}/bin/bsdtar'},
            ],
        },
    }
