@y.package
def libmetalink0():
    return {
        'code': """
             source fetch "https://launchpad.net/libmetalink/trunk/libmetalink-{version}/+download/libmetalink-{version}.tar.gz" 1
             export SHELL=`which dash` 
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static --with-libexpat=yes --with-libxml2=no || exit 1
             $YMAKE -j $NTHRS SHELL=$SHELL
             $YMAKE install
        """,
        'meta': {
            'kind': ['library'],
            'depends': ['expat', 'dash', 'make', 'c'],
            'provides': [
                {'lib': 'metalink'},
                {'configure': '--with-libmetalink={pkgroot}'},
                {'env': 'METALINK_CFLAGS', 'value': '"-I{pkgroot}/include"'},
                {'env': 'METALINK_LIBS', 'value': '"-I{pkgroot}/lib -lmetalink"'},
            ],
        },
    }
