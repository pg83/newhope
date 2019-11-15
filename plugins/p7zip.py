@y.ygenerator(tier=2, kind=['compression'])
def p7zip0():
    return {
        'code': """
             source fetch "https://downloads.sourceforge.net/p7zip/p7zip_16.02_src_all.tar.bz2" 1
             mv makefile.macosx_llvm_64bits makefile.machine
             $YMAKE -f makefile DEST_DIR=$IDIR 7za install
             cd $IDIR/usr/local/ && mv * $IDIR/
             rm -rf $IDIR/usr/local
        """,
        'version': '16.02',
    }
