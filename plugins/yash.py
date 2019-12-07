@y.ygenerator()
def yash0():
    opts = [
        '--enable-socket',
        '--enable-printf',
        '--enable-lineedit',
        '--enable-history',
        '--enable-double-bracket',
        '--enable-dirstack',
        '--enable-array',
    ]

    return {
        'code': """
            source fetch "https://osdn.net/dl/yash/yash-{version}.tar.xz" 1
            export LDFLAGS="$LDFLAGS $LIBS"
            $YSHELL ./configure --prefix=$IDIR {opts}
            $YMAKE -j2
            $YMAKE install
         """.replace('{opts}', ' '.join(opts)),
        'version': '2.49',
        'meta': {
            'kind': ['box', 'tool'],
            'depends': ['intl', 'ncurses'],
            'provides': [
                {'env': 'YSHELL_OPT', 'value': '{pkgroot}/bin/yash'},
            ],
        },
    }
