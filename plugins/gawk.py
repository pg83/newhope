@ygenerator(tier=2, kind=['base', 'dev', 'tool'])
def gawk0():
    return {
        'code': """
             source fetch "https://mirror.tochlab.net/pub/gnu/gawk/gawk-5.0.1.tar.xz" 1
             ./configure --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '5.0.1',
        'prepare': '$(ADD_PATH)',
    }
