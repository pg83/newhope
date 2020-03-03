@y.package
def autoconf0():
    return {
        'code': '''
            source fetch "https://ftp.gnu.org/gnu/autoconf/autoconf-{version}.tar.xz" 1
            $YSHELL ./configure --prefix=$MDIR
            $YMAKE -j $NTHRS
            $YMAKE DESTDIR=$IDIR install
            (cd $IDIR && mv $IDIR/$MDIR/* ./)
        ''',
        'meta': {
            'depends': ['gnu-m4', 'make'],
            'provides': [
                {'tool': 'AUTOCONF', 'value': '"{pkgroot}/bin/autoconf"'},
                {'tool': 'PERL5LIB', 'value': '"$PERL5LIB:{pkgroot}/share/autoconf"'},
            ],
        },
    }
