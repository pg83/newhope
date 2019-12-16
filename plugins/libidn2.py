@y.ygenerator()
def libidn20():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/libidn/libidn2-{version}.tar.gz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'version': '2.2.0',
        'meta': {
            'kind': ['library'],
            'depends': ['intl', 'iconv', 'libunistring', 'pkg-config'],
            'provides': [
                {'lib': 'idn2', 'configure': {'opt': '--with-libidn2={pkgroot}'}},
            ],
        },
    }
