@y.ygenerator(tier=-1, kind=['core', 'tool', 'library', 'compression'])
def bzip20():
    return {
        'code': """
            source fetch "https://sourceware.org/pub/bzip2/bzip2-1.0.8.tar.gz" 1
            $YMAKE -j2 PREFIX=$IDIR install
        """,
        'version': '1.0.8',
        'meta': {
            'provide': [
                {'lib': 'bz2'},
            ],
        },
    }
