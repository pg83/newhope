@y.ygenerator(tier=1)
def libarchive0():
    return {
        'code': """
             source fetch "https://libarchive.org/downloads/libarchive-{version}.tar.gz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '2.4.0',
        'meta': {
            'kind': ['library', 'tool', 'compression'],
            'depends': ['zlib', 'bzip2', 'xz', 'curl'],
            'provides': [
                {'lib': 'archive'}
            ],
        },
    }
