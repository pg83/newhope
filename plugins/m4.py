@y.ygenerator()
def m40():
    return {
        'code': """
               source fetch "https://ftp.gnu.org/gnu/m4/m4-{version}.tar.gz" 1
               $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-c++
               $YMAKE -j2
               $YMAKE install
        """,
        'version': '1.4.18',
        'meta': {
            'kind': ['box', 'tool'],
            'depends': ['libsigsegv'],
        },
    }
