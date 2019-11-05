@ygenerator(tier=-1, kind=['base', 'dev', 'tool'])
def gzip0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/gzip/gzip-1.10.tar.gz" 1
             export CFLAGS="-O2"
             ./configure --prefix=$IDIR --disable-gcc-warnings || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '1.10',
    }
