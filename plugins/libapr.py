@y.package
def libapr0():
    return {
        'code': """
             source fetch "https://downloads.apache.org//apr/apr-1.7.0.tar.bz2" 1
             $YSHELL ./configure $COFLAGS --prefix=$MDIR --disable-shared --enable-static --disable-dso || exit 1
             $YMAKE LIBTOOL="$LIBTOOL" -j $NTHRS
             touch .libs/libapr-1.so.0 
             $YMAKE DESTDIR=$IDIR install
             (cd $IDIR && mv $IDIR/$MDIR/* ./)
             (cd $IDIR/lib && rm *so* *.la)
        """,
        'meta': {
            'kind': ['library'],
            'depends': ['slibtool', 'make', 'c'],
            'provides': [
                {'lib': 'apr-1'},
                {'configure': '--with-libapr={pkgroot}'},
                {'configure': '--with-apr={pkgroot}'},
                {'env': 'APR_ROOT', 'value': '{pkgroot}'},
            ],
        },
    }
