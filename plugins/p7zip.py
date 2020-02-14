@y.package
def p7zip0():
    return {
        'code': '''
             source fetch "https://downloads.sourceforge.net/p7zip/p7zip_{version}_src_all.tar.bz2" 1
             cat makefile.linux_amd64  | grep -v 'PRE_COMP' | sed -e 's/CXX=.*/CXX=clang++/' | sed -e 's/CC=.*/CC=clang/' > makefile.machine
             export CFLAGS="-w $CFLAGS"
             $YMAKE -j $NTHRS -f makefile DEST_DIR=$IDIR CC=$CC CXX=$CXX ALLFLAGS_C="$CFLAGS" ALLFLAGS_CPP="$CXXFLAGS -std=c++03" LDFLAGS="$LDFLAGS $LIBS" 7za install
             (cd $IDIR/usr/local/ && mv * $IDIR/
             rm -rf $IDIR/usr/local)
             mkdir $IDIR/bin
             install bin/7za $IDIR/bin
        ''',
        'version': '16.02',
        'meta': {
            'depends': ['c++', 'make', 'c'],
            'kind': ['tool', 'library'],
            'provides': [
                {'env': 'Y7ZA', 'value': '{pkgroot}/bin/7za'},
            ],
        },
    }
