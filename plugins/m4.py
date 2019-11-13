@y.ygenerator(tier=1, kind=['core', 'box', 'tool'])
def m40():
    return {
        'code': """
               source fetch "https://ftp.gnu.org/gnu/m4/m4-1.4.18.tar.gz" 1
               $YSHELL ./configure --prefix=$IDIR --disable-c++
               $YMAKE -j2
               $YMAKE install
        """,
        'version': '1.4.18',
        'meta': {
            'depends': ['libsigsegv'],
        },
    }
