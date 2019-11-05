@ygenerator(tier=2, kind=['base', 'dev', 'library', 'tool'])
def glib0(num, info):
    return {
        'code': """
             cp -R $(MNGR_DEVTOOLS{num}_DIR)/* $BDIR/
             rm $BDIR/lib/*.la
             export CFLAGS="-I$BDIR/include -I$BDIR/lib/libffi-3.2.1/include"
             export LDFLAGS="-L$BDIR/lib"
             source fetch "http://ftp.acc.umu.se/pub/gnome/sources/glib/2.30/glib-2.30.3.tar.xz" 1
             ./configure --prefix=$IDIR --disable-shared --enable-static --with-pcre=internal --disable-nls || exit 1
             ($YMAKE -j2 && $YMAKE install) 2>&1 | grep -v 'automake-1.11: command not found'
        """.format(num=num - 1),
        'version': '2.30.3',
    }
