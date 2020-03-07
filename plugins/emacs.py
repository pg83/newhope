editor_sh='''
export EDITOR="emacsclient --socket-name $TMPDIR/emacs`id -u`/server"
'''


install_agent = '''
ln -sf ../../pkg/$1 ../../etc/runit/
ln -sf ../../pkg/$1/02-editor.sh ../../etc/profile.d/
rm -rf ./log
'''


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

             cd $IDIR
             $(F_0)
             $(F_1)
             $(F_2)
             chmod +x run
        ''',
        'extra': [
            {'kind': 'file', 'path': 'run', 'data': y.builtin_data('data/emacs_run.py')},
            {'kind': 'file', 'path': 'install', 'data': install_agent},
            {'kind': 'file', 'path': '05-editor.sh', 'data': editor_sh},
        ],
        'meta': {
            'depends': ['ncurses', 'zlib', 'make', 'c', 'autoconf', 'gnu-m4', 'perl5', 'lf-alloc'],
            'provides': [
                {'tool': 'EMACS', 'value': '"{pkgroot}/bin/emacs"'},
            ],
            'repacks': {},
        }
    }
