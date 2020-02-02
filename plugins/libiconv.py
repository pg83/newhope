@y.package
def libiconv0():
    extra = []

    if '{os}' == 'darwin':
        extra = [
            {'libs': '-framework CoreFoundation'}
        ]

    return {
        'code': """
            source fetch "https://ftp.gnu.org/pub/gnu/libiconv/libiconv-{version}.tar.gz" 1
            export LDFLAGS="$LDFLAGS $LIBS"
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared || exit 1
            $YMAKE -j $NTHRS || exit 1
            $YMAKE install
        """,
        'version': '1.16',
        'meta': {
            'kind': ['box', 'library', 'tool'],
            'provides': [
                {
                    'lib': 'iconv',
                    'configure': {
                        'opts': [
                            '--with-libiconv-prefix={pkgroot}',
                            '--with-iconv={pkgroot}',
                        ],
                    },
                    'extra': extra,
                },
                {'lib': 'charset'},
            ],
        },
    }
