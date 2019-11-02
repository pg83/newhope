@ygenerator(tier=-1, kind=['core', 'dev', 'library'])
def bzip20(deps):
    return {
        'src': 'https://sourceware.org/pub/bzip2/bzip2-1.0.8.tar.gz',
        'code': """
            $YMAKE -j2 PREFIX=$IDIR install
        """,
        'prepare': '$(ADD_PATH)',
        'deps': deps,
        'version': '1.0.8',
    }
