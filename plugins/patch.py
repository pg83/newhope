@y.package
def patch0():
    return {
        'code': '''
             source fetch "https://ftp.gnu.org/gnu/patch/patch-{version}.tar.xz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared
             $YMAKE -j $NTHRS
             $YMAKE install
        ''',
        'meta': {
            'depends': ['bison', 'make', 'c'],
            'provides': [
                {'tool': 'PATCH', 'value': '{pkgroot}/bin/patch'},
            ],
        },
    }
