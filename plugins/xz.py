@ygenerator(tier=0, kind=['core', 'dev', 'tool'], cached=['deps', 'codec'])
def xz0(deps, codec):
    return {
        'code': './configure --prefix=$IDIR --disable-shared --enable-static && make -j2 && make install',
        'prepare': '$(ADD_PATH)',
        'src': 'https://sourceforge.net/projects/lzmautils/files/xz-5.2.4.tar.gz/download',
        'deps': deps,
        'codec': codec,
        'version': '5.2.4',
    }
