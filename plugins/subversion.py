@y.package
def subversion0():
    return {
        'code': """
             source fetch "https://downloads.apache.org/subversion/subversion-1.13.0.tar.bz2" 1
             export COFLAGS="$(echo "$COFLAGS" | tr ' ' '\\n' | grep -v expat | tr '\\n' ' ')"
             export COFLAGS="$COFLAGS --with-expat=$EXPAT_DIR/include:$EXPAT_DIR/lib:-lexpat"
             export CFLAGS="-I$SQLITE3_ROOT/include $CFLAGS"
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static --with-lz4=internal || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'meta': {
            'depends': ['sqlite3', 'utf8proc', 'libapr', 'libapr-util', 'zlib', 'expat', 'make', 'c'],
            'provides': [
                {'tool': 'SVN', 'value': '{pkgroot}/bin/svn'},
            ],
            'repacks': {},
        },
    }
