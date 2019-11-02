@ygenerator(tier=0, kind=['core', 'dev', 'library', 'tool'])
def readline0(deps):
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/readline/readline-8.0.tar.gz" 1
             ./configure --prefix=$IDIR --enable-static --disable-shared
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '8.0',
        'deps': deps,
    }
