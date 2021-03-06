@y.package
def pcre10():
    return {
        'code': """
             source fetch "https://downloads.sourceforge.net/project/pcre/pcre/{version}/pcre-{version}.tar.bz2" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static --enable-pcregrep-libz --enable-pcregrep-libbz2 --enable-newline-is-anycrlf --enable-utf8 --enable-jit --enable-c++ || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'meta': {
            'depends': ['pkg-config-int', 'zlib', 'bzip2', 'c++', 'make', 'c'],
            'provides': [
                {'lib': 'pcre'},
            ],
        },
    }
