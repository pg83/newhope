def mc(gui, gui_lib):
    return {
        'code': '''
             source fetch "http://ftp.midnight-commander.org/mc-{version}.tar.xz" 1
             export LDFLAGS="$LDFLAGS $LIBS"
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static --with-screen={gui}  || exit 1
             $YMAKE -j $NTHRS
             echo 'all install:' > doc/hlp/Makefile
             $YMAKE install
        '''.replace('{gui}', gui_lib),
        'version': y.package_versions()['mc'],
        'meta': {
            'depends': ['intl', 'iconv', 'glib', gui, 'make', 'c'],
            'repacks': {},
        }
    }


@y.package
def mc_slang0():
    return mc('slang', 'slang')


@y.package
def mc_ncurses0():
    return mc('ncurses', 'ncurses')
