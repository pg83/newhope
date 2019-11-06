@ygenerator(tier=1, kind=['core', 'box', 'library', 'tool'])
def libarchive0():
    return {
        'code': """
             source fetch "https://libarchive.org/downloads/{name}-{version}.tar.gz" 1
             $YSHELL ./configure --prefix=$IDIR --enable-static --disable-shared
             $YMAKE -j2
             $YMAKE install
        """.format(name='libarchive', version='2.4.0'),
        'version': '2.4.0',
        'name': 'libarchive',
        'meta': {
            'depends': ['zlib', 'bzip2', 'xz'],
            'provides': [
                {'lib': 'libarchive'}
            ],
        },
    }
