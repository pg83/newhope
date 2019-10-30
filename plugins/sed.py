@ygenerator(tier=0, kind=['base', 'dev', 'tool'], cached=['deps'])
def sed0(deps):
    return {
        'code': """
             ./configure --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'url': 'https://ftp.gnu.org/gnu/sed/sed-4.7.tar.xz',
        'deps': deps,
        'version': '4.7',
        'prepare': '$(ADD_PATH)',
    }
