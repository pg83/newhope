@ygenerator(tier=-2, kind=['core', 'dev'])
def libsigsegv0(num):
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/libsigsegv/libsigsegv-2.12.tar.gz" 1
             ./configure --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j2
             $YMAKE install
        """.format(num=num - 1),
        'version': '3.2.1',
    }
