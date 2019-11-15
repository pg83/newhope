@y.ygenerator(tier=2, kind=['library'])
def glib0():
    return {
        'code': """
             source fetch "http://ftp.acc.umu.se/pub/gnome/sources/glib/2.30/glib-2.30.3.tar.xz" 1
             export LIBS="$LDFLAGS $LIBS"
             export CFLAGS="$CFLAGS $LDFLAGS"
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static --with-pcre=internal --with-libiconv=gnu --disable-nls || exit 1
             ($YMAKE -j2 && $YMAKE install) 2>&1 | grep -v 'automake-1.11: command not found'
        """,
        'version': '2.30.3',
        'meta': {
            'depends': ['iconv', 'intl', 'libffi', 'pkg_config_int', 'coreutils'],
            'provides': [
                {
                    'lib': 'glib-2.0', 
                    'extra': [
                        {'libs': '-framework CoreServices -framework CoreFoundation', 'os': 'darwin'}
                    ],
                },
            ],
        },
    }
