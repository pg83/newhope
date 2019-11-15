@y.ygenerator(tier=-2, kind=['box'])
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
            source fetch "https://osdn.net/dl/yash/yash-2.49.tar.xz" 1
            $YSHELL ./configure $COFLAGS --prefix=$IDIR {opts}
            $YMAKE -j2
            $YMAKE install
         """.format(opts=' '.join(opts)),
        'version': '2.49',
        'meta': {
            'depends': ['intl', 'ncurses'],
        },
    }
