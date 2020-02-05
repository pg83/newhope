@y.package
def slang0():
    return {
        'code': """
            source fetch "https://www.jedsoft.org/snapshots/slang-{version}.tar.gz" 1
            export AR_CR="$AR cr"
            $YSHELL ./configure $COFLAGS --disable-shared --enable-static  --prefix=$IDIR --with-readline=gnu --without-png --without-pcre --without-onig || exit 1
            $YMAKE AR_CR="$AR cr" install-static || exit 1
        """,
        'version': 'pre2.3.3-18',
        'meta': {
            'kind': ['library'],
            'depends': ['zlib', 'readline', 'iconv'],
            'provides': ['slang'],
        },
    }
