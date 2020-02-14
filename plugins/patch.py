@y.package
def patch0():
    return {
        'code': '''
             source fetch "https://ftp.gnu.org/gnu/patch/patch-{version}.tar.xz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared
             $YMAKE -j $THRS
             $YMAKE install
        ''',
        'version': '2.7.6',
        'meta': {
            'depends': ['bison', 'make', 'c'],
            'kind': ['tool'],
            'provides': [
                {'env': 'PATCH', 'value': '{pkgroot}/bin/patch'},
            ],
        },
    }
