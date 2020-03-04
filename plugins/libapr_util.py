@y.package
def libapr_util0():
    return {
        'code': """
             source fetch "https://downloads.apache.org//apr/apr-util-1.6.1.tar.bz2" 1

             cp $APR_ROOT/build-1/apr_rules.mk build/rules.mk
             export CFLAGS="-I$APR_ROOT/include/apr-1 $CFLAGS"

             ln -s $AR ./ar
             export PATH=$(pwd):$PATH

             $YSHELL ./configure $COFLAGS --prefix=$MDIR --disable-shared --enable-static --with-dbm=gdbm --disable-util-dso || exit 1
             $YMAKE LIBTOOL="$LIBTOOL" -j $NTHRS

             touch .libs/libaprutil-1.so.0

             $YMAKE DESTDIR=$IDIR install

             (cd $IDIR && mv $IDIR/$MDIR/* ./)
             (cd $IDIR/lib && rm *so* *.la)
        """,
        'meta': {
            'depends': ['slibtool', 'libapr', 'iconv', 'sqlite3', 'gdbm', 'make', 'expat', 'openssl', 'c'],
            'provides': [
                {'lib': 'aprutil-1'},
                {'configure': '"--with-libapr-util={pkgroot}"'},
                {'configure': '"--with-apr-util={pkgroot}"'},
            ],
        },
    }
