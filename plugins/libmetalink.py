@y.ygenerator(tier=-2)
def libmetalink0():
    return {
        'code': """
             source fetch "https://launchpad.net/libmetalink/trunk/libmetalink-{version}/+download/libmetalink-{version}.tar.gz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static --with-libexpat=yes --with-libxml2=no || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'version': '0.1.3',
        'meta': {
            'kind': ['library'],
            'depends': ['expat'],
            'provides': [
                {'lib': 'metalink', 'configure': {'opt': '--with-libmetalink={pkgroot}'}},
            ],
        },
    }
