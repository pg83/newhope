@y.ygenerator(tier=1)
def ncurses0():
    return {
        'code': """
            source fetch "https://ftp.gnu.org/pub/gnu/ncurses/ncurses-{version}.tar.gz" 1
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --without-shared --without-debug --without-ada --enable-widec --enable-pc-files --enable-overwrite --enable-ext-colors --enable-termcap --with-pkg-config --with-termlib
            $YMAKE -j2
            $YMAKE install
            cd $IDIR/lib && (for i in `ls *.a`; do q=`echo $i | tr -d 'w'`;  ln -s $i $q; done)
        """,
        'version': '6.1',
        'meta': {
            'kind': ['library'],
            'provides': [
                {'lib': 'ncurses', 'configure': {'opts': ['--with-curses={pkgroot}', '--with-ncurses={pkgroot}']}},
                {'env': 'LIBS', 'value': 'export LIBS="$LIBS -lncurses -ltinfo -lpanel -lmenu -lform"'},
            ],
        },
    }
