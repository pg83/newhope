@y.ygenerator()
def p7zip0():
    return {
        'code': """
             source fetch "https://downloads.sourceforge.net/p7zip/p7zip_{version}_src_all.tar.bz2" 1
             mv {mk} makefile.machine
             $YMAKE -j4 -f makefile DEST_DIR=$IDIR 7za install
             cd $IDIR/usr/local/ && mv * $IDIR/
             rm -rf $IDIR/usr/local
        """,
        'extra': [
            {'os': 'linux', 'value': {'kind': 'subst', 'from': '{mk}', 'to': 'makefile.linux_amd64'}},
            {'os': 'darwin', 'value': {'kind': 'subst', 'from': '{mk}', 'to': 'makefile.macosx_llvm_64bits'}},        
        ],
        'version': '16.02',
        'meta': {
            'depends': [
                'yasm',
            ],
            'kind': ['compression', 'tool', 'library'],
            'provides': [
                {'env': 'Y7ZA', 'value': '{pkgroot}/bin/7za'},
            ],
        },
    }
