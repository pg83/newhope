@ygenerator(tier=-1, kind=['core', 'library', 'tool', 'box'])
def libtools0():
    return {
        'code': """
            source fetch "http://ftpmirror.gnu.org/libtool/libtool-2.4.6.tar.gz" 1
            $YSHELL ./configure --prefix=$IDIR --enable-static --disable-shared --enable-ltdl-install || exit 1
            $YMAKE -j2 || exit 1
            $YMAKE install
        """,
        'version': '2.4.6',
        'meta': {
            'depends': [],
            'provides': [
                {'lib': 'libltdl'},
            ],
        }
    }
