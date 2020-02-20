@y.package
def slang0():
    return {
        'code': """
            source fetch "https://www.jedsoft.org/snapshots/slang-{version}.tar.gz" 1
            export AR_CR="$AR cr"
            $YSHELL ./configure $COFLAGS --disable-shared --enable-static  --prefix=$IDIR --with-readline=gnu --without-png --without-pcre --without-onig || exit 1
            $YMAKE AR_CR="$AR cr" install-static || exit 1
        """,
        'meta': {
            'kind': ['library'],
            'depends': ['zlib', 'readline', 'iconv', 'make', 'c'],
            'provides': [
                {'lib': 'slang'},
                {'env': 'SLANG_CFLAGS', 'value': '"-I{pkgroot}/include"'},
                {'env': 'SLANG_LIBS', 'value': '"-L{pkgroot}/lib -lslang"'}
            ],   
        },
    }
