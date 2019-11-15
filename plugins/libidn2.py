@y.ygenerator(tier=-2, kind=['library'])
def libidn20():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/libidn/libidn2-2.2.0.tar.gz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '2.2.0',
        'meta': {
            'depends': ['intl', 'iconv', 'libunistring', 'pkg_config'],
            'provides': [
                {'lib': 'idn2', 'configure': {'opt': '-with-libidn2={pkgroot}'}},
            ],
        },
    }
