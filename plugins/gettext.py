@y.ygenerator(tier=1, kind=['core', 'box', 'library', 'tool'])
def gettext0():
    opts = [
        '--with-included-libunistring',
        '--with-included-libxml',
        '--with-included-gettext',
        '--enable-relocatable',
        '--disable-c++',
    ]

    return {
        'code': """
            source fetch "https://ftp.gnu.org/gnu/gettext/gettext-0.20.1.tar.gz" 1
            $YSHELL ./configure --prefix=$IDIR --enable-static --disable-shared {opts} || exit 1
            $YMAKE -j2 || exit 1
            $YMAKE install
        """.format(opts=' '.join(opts)),
        'version': '0.20.1',
        'meta': {
            'depends': ['iconv', 'ncurses'],
            'soft': ['libxml2'],
            'prowide': [
                {'lib': 'intl', 'configure': {'opt': '--with-libintl-prefix={pkg_root}'}},
            ],
        },
    }
