@ygenerator(tier=0, kind=['base', 'dev', 'tool'], cached=['deps'])
def grep0(deps):
    return {
        'code': """
             ./configure --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'url': 'https://ftp.gnu.org/gnu/grep/grep-3.3.tar.xz',
        'deps': deps,
        'version': '3.3',
        'prepare': '$(ADD_PATH)',
    }
