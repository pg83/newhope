@y.package
def slibtool0():
    return {
        'code': """
             source fetch "https://github.com/midipix-project/slibtool/archive/v0.5.28.tar.gz" 0
             mv slibtool* xxx && cd xxx
             export LDFLAGS="$LDFLAGS $CFLAGS"
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'meta': {
            'kind': ['tool'],
            'depends': ['make', 'c'],
            'provides': [
                {'tool': 'LIBTOOL', 'value': '{pkgroot}/bin/slibtool'},
            ],
        },
    }
