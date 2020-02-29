@y.package
def libxml20():
    return {
        'code': '''
            source fetch "ftp://xmlsoft.org/libxml2/libxml2-{version}.tar.gz" 1
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared --without-python || 1
            $YMAKE -j $NTHRS
            $YMAKE install
        ''',
        'version': '2.9.10',
        'meta': {
            'kind': ['library'],
            'depends': ['c', 'make', 'iconv', 'zlib', 'xz', 'readline'],
            'provides': [
                {'lib': 'xml2'},
                {'configure': '--with-libxml2={pkgroot}'},
                {'configure': '--with-libxml2-prefix={pkgroot}'},
                {'env': 'LIBXML2_ROOT', 'value': '"{pkgroot}"'},
            ],
            'repacks': {},
        },
    }
