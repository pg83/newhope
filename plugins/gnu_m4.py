@y.package
def gnu_m40():
    return {
        'code': """
               source fetch "https://ftp.gnu.org/gnu/m4/m4-{version}.tar.gz" 1
               $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-c++
               echo 'all install:' > doc/Makefile
               $YMAKE -j $NTHRS
               $YMAKE install
        """,
        'version': '1.4.18',
        'meta': {
            'kind': ['tool'],
            'depends': ['libsigsegv', 'crt', 'help2man', 'make', 'c'],
            'provides': [
                {'env': 'M4', 'value': '{pkgroot}/bin/m4'},
            ],
        },
    }
