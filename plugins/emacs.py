#@y.package
def emacs0():
    return {
        'code': '''
             source fetch "https://ftp.gnu.org/gnu/emacs/emacs-{version}.tar.xz" 1
             $YSHELL ./configure --prefix=$IDIR --enable-static --disable-shared --without-all --without-x || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        ''',
        'meta': {
            'kind': ['tool'],
            'depends': ['ncurses', 'zlib', 'make', 'c'],
            'provides': [
                {'tool': 'EMACS', 'value': '"{pkgroot/bin/emacs}"'},
            ],
        }
    }
