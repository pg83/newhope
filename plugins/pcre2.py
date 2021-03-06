@y.package
def pcre20():
    return {
        'code': """
             source fetch "https://ftp.pcre.org/pub/pcre/pcre2-{version}.tar.bz2" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static --enable-pcregrep-libz --enable-pcregrep-libbz2 --enable-newline-is-anycrlf --enable-utf8 --enable-jit --enable-c++ || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'meta': {
            'depends': ['pkg-config-int', 'zlib', 'bzip2', 'c++', 'make', 'c'],
            'provides': [
                {'lib': 'pcre2-8'},
                {'env': 'LIBPCRE2_INCLUDES', 'value': '"-I{pkgroot}/include"'},
                {'env': 'PCRE2_CFLAGS', 'value': '"-I{pkgroot}/include"'},
                {'env': 'PCRE2_LIBS', 'value': '"-L{pkgroot}/lib -lpcre2-8"'},
            ],
        },
    }
