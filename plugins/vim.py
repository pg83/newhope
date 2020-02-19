@y.package
def vim0():
    return {
        'code': '''
             source fetch "https://github.com/vim/vim/archive/v{version}.tar.gz" 0
             (mv vim* xxx && mv xxx/* ./)
             $YSHELL ./configure --prefix=$IDIR --enable-static --disable-shared || exit 1
             $YMAKE -j $THRS
             $YMAKE install
             ($YUPX $IDIR/bin/*) || true
        ''',
        'version': '8.2.0268',
        'meta': {
            'kind': ['tool'],
            'depends': ['ncurses', 'zlib', 'make', 'c', 'upx'],
            'provides': [
                {'env': 'VIM', 'value': '"{pkgroot}/bin/vim"'},
            ],
        }
    }
