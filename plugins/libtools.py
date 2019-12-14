@y.ygenerator()
def libtools0():
    return {
        'code': """
            source fetch "http://ftpmirror.gnu.org/libtool/libtool-{version}.tar.gz" 1
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared --enable-ltdl-install || exit 1
            $YMAKE -j2 || exit 1
            $YMAKE install
        """,
        'version': '2.4.6',
        'meta': {
            'kind': ['library', 'tool', 'box'],
            'depends': ['m4'],
        }
    }
