@y.package
def texinfo0():
    return {
        'code': """
             source fetch "http://ftp.gnu.org/gnu/texinfo/texinfo-{version}.tar.xz" 1
             export PERL="$YPERL"
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'meta': {
            'depends': ['c++', 'make', 'c', 'perl5'],
            'provides': [
                {'tool': 'MAKEINFO', 'value': '{pkgroot}/bin/makeinfo'},
            ],
        }
    }
