@ygenerator(tier=-1, kind=['core', 'dev', 'library'])
def bzip20():
    return {
        'src': 'https://sourceware.org/pub/bzip2/bzip2-1.0.8.tar.gz',
        'code': """
            $YMAKE -j2 PREFIX=$IDIR install
        """,
        'prepare': '$(ADD_PATH)',
        'version': '1.0.8',
    }
