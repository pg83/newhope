#@ygenerator(tier=3, kind=['core', 'dev', 'library'])
def openssl0():
    return {
        'code': """
            source fetch "https://www.openssl.org/source/old/1.1.1/openssl-1.1.1c.tar.gz" 1
            ./configure --prefix=$IDIR
            $YMAKE -j2
            $YMAKE install
        """,
        'version': '1.1.1c',
    }
