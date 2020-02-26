@y.package
def vim0():
    return {
        'code': '''
             source fetch "https://github.com/vim/vim/archive/v{version}.tar.gz" 0
             (mv vim* xxx && mv xxx/* ./)
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
             ($YUPX $IDIR/bin/*) || true
        ''',
        'meta': {
            'kind': ['tool'],
            'depends': ['ncurses', 'zlib', 'make', 'c', 'upx'],
            'provides': [
                {'tool': 'VIM', 'value': '"{pkgroot}/bin/vim"'},
            ],
        }
    }
