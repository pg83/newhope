@ygenerator(tier=-2, kind=['core', 'dev', 'tool'])
def dash0():
    return {
        'code': """
            source fetch "http://gondor.apana.org.au/~herbert/dash/files/dash-0.5.10.2.tar.gz" 1
            ./configure --prefix=$IDIR
            $YMAKE -j2
            $YMAKE install
         """,
        'version': '0.5.10.2',
    }
