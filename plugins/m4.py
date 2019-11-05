@ygenerator(tier=1, kind=['core', 'dev', 'tool'])
def m40():
    return {
        'code': """
               source fetch "https://ftp.gnu.org/gnu/m4/m4-1.4.18.tar.gz" 1
               ./configure --prefix=$IDIR
               $YMAKE -j2
               $YMAKE install
        """,
        'version': '1.4.18',
    }
