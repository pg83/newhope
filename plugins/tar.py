@ygenerator(tier=0, kind=['core', 'dev', 'tool'])
def tar0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/tar/tar-1.32.tar.gz" 1
             FORCE_UNSAFE_CONFIGURE=1 ./configure --prefix=$IDIR && $YMAKE -j2 && $YMAKE install
        """,
        'version': '1.32',
    }
