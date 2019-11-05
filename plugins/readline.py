@ygenerator(tier=0, kind=['core', 'dev', 'library', 'tool'])
def readline0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/readline/readline-8.0.tar.gz" 1
             ./configure --prefix=$IDIR --enable-static --disable-shared
             $YMAKE -j2
             $YMAKE install 2>&1 | grep -v 'No such file or directory'
        """,
        'version': '8.0',
    }
