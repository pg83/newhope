@ygenerator(tier=3, kind=['base', 'dev', 'tool'])
def mc0(deps, num):
    return {
        'code': """
             source fetch "http://ftp.midnight-commander.org/mc-4.8.23.tar.xz" 1
             cp -R $(MNGR_DEVTOOLS{num}_DIR)/* $BDIR/runtime/
             rm $BDIR/runtime/lib/*.la
             export CFLAGS="-I$BDIR/runtime/include/glib-2.0 -I$BDIR/runtime/lib/glib-2.0/include $CFLAGS"
             export LDFLAGS="-L$BDIR/runtime/lib $LDFLAGS"
             export LIBS="-framework CoreServices -framework CoreFoundation -lglib-2.0 -lintl -liconv"
             ./configure --prefix=$IDIR --disable-shared --enable-static --with-screen=ncurses --with-libiconv-prefix=$BDIR/runtime --with-libintl-prefix=$BDIR/runtime || exit 1
             $YMAKE -j2
             $YMAKE install
        """.format(num=num-1),
        'deps': deps,
        'version': '4.8.23',
        'prepare': '$(ADD_PATH)',
    }
