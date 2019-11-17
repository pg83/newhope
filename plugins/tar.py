@y.ygenerator(tier=0)
def tar0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/tar/tar-{version}.tar.gz" 1
             export FORCE_UNSAFE_CONFIGURE=1 
             $YSHELL ./configure $COFLAGS --prefix=$IDIR
             $YMAKE -j2 && $YMAKE install
        """,
        'version': '1.32',
        'meta': {
            'kind': ['compression'],
            'depends': ['iconv', 'intl', 'gzip', 'bzip2', 'xz', 'unrar'],
        },
    }
