@y.ygenerator(tier=-1, kind=['core', 'library'])
def slang0():
    return {
        'code': """
            source fetch "https://www.jedsoft.org/snapshots/slang-pre2.3.3-15.tar.gz" 1
            $YSHELL ./configure --disable-shared --enable-static  --prefix=$IDIR --with-readline=gnu || exit 1
            $YMAKE -j2 && $YMAKE install
        """,
        'version': 'pre2.3.3-15',
        'meta': {
            'depends': [],
            'provides': ['slang'],
        },
    }
