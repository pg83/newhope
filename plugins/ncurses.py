@y.ygenerator()
def ncurses0():
    return {
        'code': """
            source fetch "https://ftp.gnu.org/pub/gnu/ncurses/ncurses-{version}.tar.gz" 1
            source add_strip
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --without-shared --without-debug --without-ada --enable-widec --enable-pc-files --enable-overwrite --enable-ext-colors --enable-termcap --with-pkg-config --with-termlib --without-cxx --without-cxx-binding
            $YMAKE -j $NTHRS || true
            $YMAKE -j $NTHRS
            mv install install-tmp
            ln -s install-sh install
            $YMAKE install

            cd $IDIR/lib && (for i in `ls *.a`; do q=`echo $i | tr -d 'w'`;  ln -s $i $q; done)
        """,
        'version': '6.1',
        'meta': {
            'kind': ['library'],
            'depends': ['slibtool'],
            'provides': [
                {'lib': 'ncurses', 'configure': {'opts': ['--with-curses={pkgroot}', '--with-ncurses={pkgroot}']}},
                {'env': 'LIBS', 'value': '"$LIBS -lncurses -ltinfo -lpanel -lmenu -lform"'},
            ],
        },
    }
