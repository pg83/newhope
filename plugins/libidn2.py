@y.package
def libidn20():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/libidn/libidn2-{version}.tar.gz" 1

             ln -s "$CC" ./gcc
             ln -s "$CC" ./cc
             export PATH="$(pwd):$PATH"

             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'meta': {
            'kind': ['library'],
            'depends': ['intl', 'iconv', 'libunistring', 'pkg-config', 'make', 'c'],
            'provides': [
                {'lib': 'idn2', 'configure': {'opt': '--with-libidn2={pkgroot}'}},
            ],
        },
    }
