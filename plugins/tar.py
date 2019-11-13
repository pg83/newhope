@y.ygenerator(tier=0, kind=['core', 'tool', 'compression'])
def tar0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/tar/tar-1.32.tar.gz" 1
             export FORCE_UNSAFE_CONFIGURE=1 
             $YSHELL ./configure --prefix=$IDIR
             $YMAKE -j2 && $YMAKE install
        """,
        'version': '1.32',
        'meta': {
            'depends': ['iconv', 'intl', 'gzip', 'bzip2', 'xz', 'unrar'],
        },
    }
