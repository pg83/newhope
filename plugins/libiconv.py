@ygenerator(tier=0, kind=['core', 'dev', 'library'], cached=['deps'])
def libiconv0(deps):
    return {
        'code': """
            source fetch "https://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.16.tar.gz" 1
            ./configure --prefix=$IDIR --enable-static --disable-shared || exit 1
            make -j2 || exit 1
            make install
        """,
        'prepare': '$(ADD_PATH)',
        'deps': deps,
        'version': '1.16',
    }
