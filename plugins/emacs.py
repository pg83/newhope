@y.package
def emacs0():
    return {
        'code': '''
             source fetch "https://ftp.gnu.org/gnu/emacs/emacs-{version}.tar.xz" 1
             export CC="$CC -I. -I../src -I../lib -I../lib-src"
             export CFLAGS="-fno-pie -D_GNU_SOURCE=1 -I. -I../src -I../lib -I../lib-src $CFLAGS -fno-pie"
             export LDFLAGS="-no-pie $LDFLAGS -no-pie"
             $YSHELL ./configure --prefix=$IDIR --enable-static --disable-shared --without-all --without-x || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        ''',
        'meta': {
            'kind': ['tool'],
            'depends': ['ncurses', 'zlib', 'make', 'c', 'tcmalloc'],
            'provides': [
                {'tool': 'EMACS', 'value': '"{pkgroot}/bin/emacs"'},
            ],
            'repacks': {},
        }
    }
