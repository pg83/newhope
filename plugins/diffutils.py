@ygenerator(tier=2, kind=['core', 'dev', 'tool'], cached=['deps'])
def diffutils0(deps):
    version = '3.7'
    url = 'https://ftp.gnu.org/gnu/diffutils/diffutils-' + version + '.tar.xz'

    return {
        'code': """
             ./configure --prefix=$IDIR --disable-shared --enable-static || exit 1
             make -j2
             make install
        """,
        'url': url,
        'deps': deps,
        'version': version,
        'prepare': '$(ADD_PATH)',
    }
