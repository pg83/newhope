@y.ygenerator()
def p7zip0():
    return {
        'code': """
             source fetch "https://downloads.sourceforge.net/p7zip/p7zip_{version}_src_all.tar.bz2" 1
             mv makefile.macosx_llvm_64bits makefile.machine
             $YMAKE -f makefile DEST_DIR=$IDIR 7za install
             cd $IDIR/usr/local/ && mv * $IDIR/
             export Y7ZA=$IDIR/bin/7za
             rm -rf $IDIR/usr/local
        """,
        'version': '16.02',
        'meta': {
            'kind': ['compression', 'tool'],
            'flags': ['HAVE_7ZA_BIN'],
            'provides': [
                {'env': 'Y7ZA', 'value': '{pkgroot}/bin/7za'},
            ],
        },
    }
