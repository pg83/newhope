#@ygenerator(tier=1, kind=['base', 'dev', 'library'], cached=['deps'])
def glib0(deps):
    return {
        'code': """
             ./configure --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j2
             $YMAKE install
        """,
        'url': 'http://ftp.gnome.org/pub/gnome/sources/glib/2.62/glib-2.62.2.tar.xz',
        'deps': deps,
        'version': '2.62.2',
        'prepare': '$(ADD_PATH)',
    }
