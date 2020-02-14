@y.package
def texinfo0():
    return {
        'code': """
             source fetch "http://ftp.gnu.org/gnu/texinfo/texinfo-{version}.tar.xz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'version': '6.7',
        'meta': {
            'kind': ['tool'],
            'depends': ['c++', 'make', 'c'],
            'provides': [
                {'env': 'MAKEINFO', 'value': '{pkgroot}/bin/makeinfo'},
            ],
        }
    }
