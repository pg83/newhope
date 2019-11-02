@ygenerator(tier=0, kind=['core', 'dev', 'library'])
def libtools0(deps):
    return {
        'code': """
            source fetch "http://ftpmirror.gnu.org/libtool/libtool-2.4.6.tar.gz" 1
            ./configure --prefix=$IDIR --enable-static --disable-shared || exit 1
            $YMAKE -j2 || exit 1
            $YMAKE install
        """,
        'prepare': '$(ADD_PATH)',
        'deps': deps,
        'version': '2.4.6',
    }
