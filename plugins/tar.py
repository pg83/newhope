@ygenerator(tier=0, kind=['core', 'dev', 'tool'])
def tar0(deps):
    return {
        'code': 'FORCE_UNSAFE_CONFIGURE=1 ./configure --prefix=$IDIR && $YMAKE -j2 && $YMAKE install',
        'prepare': '$(ADD_PATH)',
        'src': 'https://ftp.gnu.org/gnu/tar/tar-1.32.tar.gz',
        'deps': deps,
        'version': '1.32',
    }
