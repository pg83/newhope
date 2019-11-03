@ygenerator(tier=0, kind=['base', 'dev', 'tool'])
def sed0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/sed/sed-4.7.tar.xz" 1
             ./configure --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '4.7',
        'prepare': '$(ADD_PATH)',
    }
