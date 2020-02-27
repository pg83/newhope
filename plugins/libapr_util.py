#@y.package
def libapr_util0():
    return {
        'code': """
             source fetch "https://downloads.apache.org//apr/apr-util-1.6.1.tar.bz2" 1
             cp $APR_ROOT/build-1/apr_rules.mk build/rules.mk
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static --with-dbm=gdbm --disable-util-dso || exit 1
             $YMAKE LIBTOOL="$LIBTOOL" -j $NTHRS
             $YMAKE install
        """,
        'meta': {
            'kind': ['library'],
            'depends': ['libapr', 'iconv', 'sqlite3', 'gdbm', 'make', 'expat', 'openssl', 'c'],
            'provides': [
                {'lib': 'apr_util'},
                {'configure': '--with-libapr-util={pkgroot}'},
            ],
        },
    }
