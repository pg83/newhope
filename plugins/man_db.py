@y.package
def man_db0():
    return {
        'code': """
            source fetch "http://deb.debian.org/debian/pool/main/m/man-db/man-db_2.9.0.orig.tar.xz" 1
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-shared --disable-static || exit 1
            $YMAKE -j $THRS
            $YMAKE install
        """,
        'meta': {
            'kind': ['tool'],
            'depends': ['libpipeline', 'gdbm'],
        },
    }
