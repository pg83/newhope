@y.ygenerator(tier=-2)
def libiconv0():
    return {
        'code': """
            source fetch "https://ftp.gnu.org/pub/gnu/libiconv/libiconv-{version}.tar.gz" 1
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared || exit 1
            $YMAKE -j2 || exit 1
            $YMAKE install
        """,
        'version': '1.16',
        'meta': {
            'kind': ['box'],
            'depends': [],
            'provides': [
                {'lib': 'iconv', 'configure': {'opts': ['--with-libiconv-prefix={pkgroot}', '--with-iconv={pkgroot}']}},
                {'lib': 'charset'},
            ],
        },
    }
