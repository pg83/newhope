@y.package
def procps_ng0():
    return {
        'code': '''
             source fetch "https://downloads.sourceforge.net/project/procps-ng/Production/procps-ng-{version}.tar.xz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared --disable-numa
             $YMAKE -j $NTHRS
             $YMAKE install
             $YUPX $IDIR/bin/*
        ''',
        'meta': {
            'depends': ['make', 'c', 'ncurses', 'intl', 'iconv', 'upx'],
            'provides': [
                {'tool': 'PATCH', 'value': '{pkgroot}/bin/patch'},
            ],
        },
    }
