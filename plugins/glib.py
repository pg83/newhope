@y.ygenerator(tier=2, kind=['core', 'library', 'tool'])
def glib0():
    return {
        'code': """
             source fetch "http://ftp.acc.umu.se/pub/gnome/sources/glib/2.30/glib-2.30.3.tar.xz" 1
             $YSHELL ./configure --prefix=$IDIR --disable-shared --enable-static --with-pcre=internal --with-libiconv=gnu || exit 1
             ($YMAKE -j2 && $YMAKE install) 2>&1 | grep -v 'automake-1.11: command not found'
        """,
        'version': '2.30.3',
        'meta': {
            'depends': ['iconv', 'intl', 'libffi', 'pkg_config_int', 'python'],
            'provide': [
                {'lib': 'glib-2.0', 'extra': {'libs': '-framework CoreServices -framework CoreFoundation', 'os': 'darwin'}},
            ],
        },
    }
