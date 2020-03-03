@y.package
def gettext0():
    opts = [
        #'--with-included-libunistring',
        '--with-included-libxml',
        '--with-included-gettext',
        '--enable-relocatable',
        '--disable-c++',
    ]

    return {
        'code': """
            source fetch "https://ftp.gnu.org/gnu/gettext/gettext-{version}.tar.gz" 1
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared {opts} || exit 1
            $YMAKE -j $NTHRS || exit 1
            $YMAKE install
            ($YUPX $IDIR/bin/*) || true
        """.replace('{opts}', ' '.join(opts)),
        'meta': {
            'depends': ['bsdtar', 'upx', 'libunistring', 'iconv', 'ncurses', 'make', 'c'],
            'provides': [
                {'lib': 'intl'},
                {'configure': '--with-libintl-prefix={pkgroot}'},
                {'tool': 'XGETTEXT', 'value': '{pkgroot}/bin/xgettext'},
            ],
        },
    }
