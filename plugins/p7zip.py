@ygenerator(tier=2, kind=['core', 'tool', 'compression'])
def p7zip0():
    return {
        'code': """
             source fetch "https://downloads.sourceforge.net/p7zip/p7zip_16.02_src_all.tar.bz2" 1
             $YMAKE -f makefile 7za
             $YMAKE make -f makefile DEST_HOME=/ DEST_MAN=/share/man DEST_SHARE_DOC=/share/doc/p7zip-16.02 install
        """,
        'version': '16.02',
    }