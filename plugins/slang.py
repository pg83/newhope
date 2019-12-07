@y.ygenerator()
def slang0():
    return {
        'code': """
            source fetch "https://www.jedsoft.org/snapshots/slang-{version}.tar.gz" 1
            $YSHELL ./configure $COFLAGS --disable-shared --enable-static  --prefix=$IDIR --with-readline=gnu --without-png --without-pcre --without-onig || exit 1
            $YMAKE install-static || exit 1
        """,
        'version': 'pre2.3.3-15',
        'meta': {
            'kind': ['library'],
            'depends': ['zlib', 'readline', 'iconv'],
            'provides': ['slang'],
        },
    }
