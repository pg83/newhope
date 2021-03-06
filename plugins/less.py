@y.package
def less0():
    return {
        'code': """
             source fetch "http://www.greenwoodsoftware.com/less/less-{version}.tar.gz" 1
             export LDFLAGS="$LDFLAGS $LIBS"
             export CFLAGS="-Dwinch=winch_ $CFLAGS"
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'meta': {
            'depends': ['ncurses', 'make', 'c'],
            'profides': [
                {'tool': 'LESS', 'value': '{pkgroot}/bin/less'}
            ],
        },
    }
