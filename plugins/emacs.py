@y.package
def emacs0():
    return {
        'code': '''
             source fetch "https://github.com/emacs-mirror/emacs/archive/emacs-27.0.90.tar.gz" 1

             ./autogen.sh

             export CC="$CC -I. -I../src -I../lib -I../lib-src"
             export CFLAGS="-fno-pie -D_GNU_SOURCE=1 -I. -I../src -I../lib -I../lib-src $CFLAGS -fno-pie"
             export LDFLAGS="-no-pie $LDFLAGS -no-pie"
 
             $YSHELL ./configure --prefix=$IDIR --enable-static --disable-shared --without-all --without-x --with-dumping=pdumper || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        ''',
        'meta': {
            'kind': ['tool'],
            'depends': ['ncurses', 'zlib', 'make', 'c', 'autoconf', 'gnu-m4', 'perl5', 'lf-alloc'],
            'provides': [
                {'tool': 'EMACS', 'value': '"{pkgroot}/bin/emacs"'},
            ],
            'repacks': {},
        }
    }
