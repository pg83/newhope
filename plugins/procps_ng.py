@y.package
def procps_ng0():
    return {
        'code': '''
             source fetch "https://downloads.sourceforge.net/project/procps-ng/Production/procps-ng-{version}.tar.xz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared --disable-numa
             $YMAKE -j $THRS
             $YMAKE install
        ''',
        'version': '3.3.16',
        'meta': {
            'depends': ['make', 'c', 'ncurses', 'intl', 'iconv'],
            'kind': ['tool'],
            'provides': [
                {'env': 'PATCH', 'value': '{pkgroot}/bin/patch'},
            ],
        },
    }
