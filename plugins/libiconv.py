@y.ygenerator()
def libiconv0():
    return {
        'code': """
            source fetch "https://ftp.gnu.org/pub/gnu/libiconv/libiconv-{version}.tar.gz" 1
            #export LDFLAGS="$LDFLAGS $LIBS"
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared || exit 1
            $YMAKE -j4 || true
            (cd lib && $YMAKE -j4 install) || exit 1
            (cd libcharset && $YMAKE -j4 install) || exit 1
            mkdir $IDIR/include || true
            cp include/* $IDIR/include/
            #$YMAKE -j2 || exit 1
            #$YMAKE install
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
                    'extra': [
                        {
                            'libs': '-framework CoreFoundation',
                            'os': 'darwin',
                        },
                    ],
                },
                {'lib': 'charset'},
            ],
        },
    }
