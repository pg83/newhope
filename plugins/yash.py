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
            export CFLAGS="-Dwordfree=yash_wordfree $CFLAGS"
            $YSHELL ./configure --prefix=$IDIR {opts}
            echo 'install-rec:' > doc/Makefile
            $YMAKE -j $NTHRS
            $YMAKE install

            echo '#!{pkgroot}/bin/yash' > $IDIR/install
            echo 'ln -lf {pkgroot}/bin/yash /etc/alt/sh' >> $IDIR/install
         """.replace('{opts}', ' '.join(opts)),
        'version': '2.49',
        'meta': {
            'kind': ['box', 'tool'],
            'depends': ['intl', 'ncurses', 'xz', 'tar', 'asciidoc', 'python'],
            'provides': [
                {'env': 'YSHELL_OPT', 'value': '{pkgroot}/bin/yash'},
                {'env': 'YASH', 'value': '{pkgroot}/bin/yash'},
            ],
        },
    }
