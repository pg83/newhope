@ygenerator(tier=2, kind=['core', 'dev', 'tool'])
def diffutils0():
    version = '3.7'
    url = 'https://ftp.gnu.org/gnu/diffutils/diffutils-' + version + '.tar.xz'

    return {
        'code': """
             ./configure --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'url': url,
        'version': version,
        'prepare': '$(ADD_PATH)',
    }
