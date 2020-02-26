@y.package
def autoconf0():
    return {
        'code': '''
            source fetch "https://ftp.gnu.org/gnu/autoconf/autoconf-{version}.tar.xz" 1
            $YSHELL ./configure --prefix=$IDIR
            $YMAKE -j $NTHRS
            $YMAKE install
        ''',
        'meta': {
            'kind': ['tool'],
            'depends': ['gnu-m4', 'make'],
            'provides': [
                {'tool': 'AUTOCONF', 'value': '"{pkgroot}/bin/autoconf"'},
            ],
        },
    }
