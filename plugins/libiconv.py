@ygenerator(tier=-1, kind=['core', 'dev', 'library'])
def libiconv0():
    return {
        'code': """
            source fetch "https://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.16.tar.gz" 1
            ./configure --prefix=$IDIR --enable-static --disable-shared || exit 1
            $YMAKE -j2 || exit 1
            $YMAKE install
        """,
        'prepare': '$(ADD_PATH)',
        'version': '1.16',
    }
