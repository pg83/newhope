@ygenerator(tier=0, kind=['base', 'dev', 'tool'])
def grep0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/grep/grep-3.3.tar.xz" 1
             ./configure --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '3.3',
        'prepare': '$(ADD_PATH)',
    }
