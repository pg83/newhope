#if defined(__LINUX__)
    @y.package
    def pcre20():
        return {
            'code': """
                 source fetch "https://downloads.sourceforge.net/project/pcre/pcre/{version}/pcre-{version}.tar.bz2" 1
                 $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static --enable-pcregrep-libz --enable-pcregrep-libbz2 --enable-newline-is-anycrlf --enable-utf8 --enable-jit --enable-c++ || exit 1
                 $YMAKE -j $NTHRS
                 $YMAKE install
            """,
            'version': '8.43',
            'meta': {
                'kind': ['library'],
                'depends': ['pkg-config-int', 'zlib', 'bzip2', 'c++'],
                'provides': [
                    {'lib': 'pcre'},
                ],
            },
        }
#endif
