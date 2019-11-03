@ygenerator(tier=0, kind=['base', 'dev'])
def libffi0(num):
    return {
        'code': """
             source fetch "https://sourceware.org/ftp/libffi/libffi-3.2.1.tar.gz" 1
             ./configure --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j2
             $YMAKE install
        """.format(num=num - 1),
        'version': '3.2.1',
        'prepare': '$(ADD_PATH)',
    }
