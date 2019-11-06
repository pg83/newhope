@ygenerator(tier=-1, kind=['core', 'tool', 'compression'])
def gzip0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/gzip/gzip-1.10.tar.gz" 1
             $YSHELL ./configure --prefix=$IDIR --disable-gcc-warnings || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '1.10',
        'meta': {
            'depends': []
        },
    }
