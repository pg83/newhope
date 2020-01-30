@y.package
def m40():
    return {
        'code': """
               source fetch "https://ftp.gnu.org/gnu/m4/m4-{version}.tar.gz" 1
               $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-c++
               $YMAKE -j $NTHRS
               $YMAKE install
        """,
        'version': '1.4.18',
        'meta': {
            'kind': ['tool'],
            'depends': ['libsigsegv'],
            'provides': [
                {'env': 'M4', 'value': '{pkgroot}/bin/m4'},
            ],
        },
    }
