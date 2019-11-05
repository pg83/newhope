@ygenerator(tier=2, kind=['core', 'dev', 'tool'])
def bison0():
    version = '3.4.2'
    url = 'https://ftp.gnu.org/gnu/bison/bison-' + version + '.tar.xz'

    return {
        'code': """
             ./configure --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'url': url,
        'version': version,
    }
