@y.ygenerator()
def glib0():
    return {
        'code': """
             source fetch "http://ftp.acc.umu.se/pub/gnome/sources/glib/2.30/glib-{version}.tar.xz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static --with-pcre=internal --with-libiconv=gnu --disable-nls || exit 1
             (
                $YMAKE -j2 || exit 1
                $YMAKE install
             ) 2>&1 | grep -v 'automake-1.11: command not found'
        """,
        'version': '2.30.3',
        'meta': {
            'kind': ['library'],
            'depends': ['iconv', 'intl', 'libffi', 'pkg-config-int', 'coreutils', 'python'],
            'provides': [
                {
                    'lib': 'glib-2.0', 
                    'extra': [
                        {'libs': '-framework CoreServices -framework CoreFoundation', 'os': 'darwin'},
                        {'ipath': '{pkgroot}/include/glib-2.0'},
                        {'ipath': '{pkgroot}/lib/glib-2.0/include'},
                    ],
                },
            ],
        },
    }
