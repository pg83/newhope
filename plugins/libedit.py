@y.package
def libedit0():
    return {
        'code': """
             source fetch "http://thrysoee.dk/editline/libedit-{version}.tar.gz" 1
             export CFLAGS="-D__STDC_ISO_10646__=1 $CFLAGS"
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'meta': {
            'kind': ['library'],
            'depends': ['ncurses', 'termcap', 'make', 'c'],
            'provides': [
                {'lib': 'edit'},
                {'configure': '--with-libedit={pkgroot}'},
            ],
        },
    }
