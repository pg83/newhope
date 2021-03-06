@y.package
def texinfo0():
    return {
        'code': """
             source fetch "http://ftp.gnu.org/gnu/texinfo/texinfo-{version}.tar.xz" 1
             export PERL="$YPERL"
             $YSHELL ./configure $COFLAGS --prefix=$MDIR --enable-static --disable-shared || exit 1
             $YMAKE -j $NTHRS
             $YMAKE DESTDIR=$IDIR install
             (cd $IDIR && mv $IDIR/$MDIR/* ./)
        """,
        'meta': {
            'depends': ['c++', 'make', 'c', 'perl5'],
            'provides': [
                {'tool': 'MAKEINFO', 'value': '{pkgroot}/bin/makeinfo'},
                {'tool': 'PERL5LIB', 'value': '"$PERL5LIB:{pkgroot}/share/texinfo"'},
            ],
        }
    }
