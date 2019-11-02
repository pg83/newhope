@ygenerator(tier=-1, kind=['base', 'dev', 'tool'])
def gzip0(deps):
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/gzip/gzip-1.10.tar.gz" 1
             ./configure --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'deps': deps,
        'version': '1.10',
        'prepare': '$(ADD_PATH)',
    }
