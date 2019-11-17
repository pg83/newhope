@y.ygenerator(tier=-1)
def bzip20():
    return {
        'code': """
            source fetch "https://sourceware.org/pub/bzip2/bzip2-{version}.tar.gz" 1
            $YMAKE -j2 PREFIX=$IDIR install
        """,
        'version': '1.0.8',
        'meta': {
            'kind': ['library', 'compression'],
            'provide': [
                {'lib': 'bz2'},
            ],
        },
    }
