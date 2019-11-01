@ygenerator(tier=-1, kind=['core', 'dev', 'library'], cached=['deps'])
def zlib0(deps):
    return {
        'src': 'http://zlib.net/zlib-1.2.11.tar.gz',
        'code': """
            ./configure --static --64 --prefix=$IDIR || exit 1
            $YMAKE -j2 && $YMAKE install
        """,
        'prepare': '$(ADD_PATH)',
        'deps': deps,
        'version': '1.2.11',
    }
