@ygenerator(tier=0, kind=['core', 'dev', 'tool'])
def xz0():
    return {
        'code': './configure --prefix=$IDIR --disable-shared --enable-static && $YMAKE -j2 && $YMAKE install',
        'prepare': '$(ADD_PATH)',
        'src': 'https://sourceforge.net/projects/lzmautils/files/xz-5.2.4.tar.gz/download',
        'version': '5.2.4',
    }
