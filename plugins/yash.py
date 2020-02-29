@y.package
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
            source fetch "https://github.com/magicant/yash/archive/ae772d184ae4362df66f646fc6b7ff8164030a7b.zip" 0
            mv ./yash* ./xxx
            mv ./xxx/* ./
            export LDFLAGS="$LDFLAGS $LIBS"
            export CFLAGS="-Dwordfree=yash_wordfree -Dadd_history=yash_add_history $CFLAGS"
            $YSHELL ./configure --prefix=$IDIR {opts}
            echo 'install-rec:' > doc/Makefile
            $YMAKE -j $NTHRS
            $YMAKE install
         """.replace('{opts}', ' '.join(opts)),
        'meta': {
            'kind': ['tool'],
            'depends': ['intl', 'ncurses', 'xz', 'tar', 'asciidoc', 'python', 'make', 'c'],
            'provides': [
                {'tool': 'YSHELL_OPT', 'value': '{pkgroot}/bin/yash'},
                {'tool': 'YASH', 'value': '{pkgroot}/bin/yash'},
            ],
        },
    }
