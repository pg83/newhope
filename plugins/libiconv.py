@y.ygenerator(tier=-2, kind=['core', 'box', 'library', 'tool'])
def libiconv0():
    return {
        'code': """
            source fetch "https://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.16.tar.gz" 1
            $YSHELL ./configure --prefix=$IDIR --enable-static --disable-shared --enable-relocatable || exit 1
            $YMAKE -j2 || exit 1
            $YMAKE install
        """,
        'version': '1.16',
        'meta': {
            'depends': [],
            'provides': [
                {'lib': 'iconv', 'configure': {'opt': ['--with-libiconv-prefix={pkg_root}', '--with-iconv={pkg_root}']}},
                {'lib': 'charset'},
            ],
        },
    }
