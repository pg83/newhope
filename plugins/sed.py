@y.package
def sed0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/sed/sed-{version}.tar.xz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'version': '4.7',
        'meta': {
            'kind': ['tool'],
            'depends': ['iconv', 'intl', 'make', 'c'],
            'provides': [
                {'env': 'SED', 'value': '{pkgroot}/bin/sed'},
            ],
        }
    }
