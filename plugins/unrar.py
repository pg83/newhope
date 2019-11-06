@ygenerator(tier=1, kind=['core', 'tool', 'compression'])
def unrar0():
    return {
        'code': """
             source fetch "http://www.rarlab.com/rar/unrarsrc-5.8.3.tar.gz" 1
             $YMAKE -f makefile
             mkdir -p $IDIR/bin
             install -v -m755 unrar $IDIR/bin
        """,
        'version': '5.8.3',
        'meta': {},
    }
