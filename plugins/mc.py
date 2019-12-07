def mc(gui):
    return {
        'code': """
             source fetch "http://ftp.midnight-commander.org/mc-{version}.tar.xz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static --with-screen={gui}  || exit 1
             $YMAKE -j2
             $YMAKE install
        """.replace('{gui}', gui),
        'version': '4.8.23',
        'meta': {
            'kind': ['program'],
            'depends': ['intl', 'iconv', 'glib', gui],
        }
    }


@y.ygenerator()
def mc_slang0():
    return mc('slang')


@y.ygenerator()
def mc_ncurses0():
    return mc('ncurses')
