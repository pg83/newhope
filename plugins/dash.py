@y.ygenerator(tier=-2, kind=['core', 'box', 'tool'])
def dash0():
    return {
        'code': """
            source fetch "http://gondor.apana.org.au/~herbert/dash/files/dash-0.5.10.2.tar.gz" 1
            $YSHELL ./configure --prefix=$IDIR
            $YMAKE -j2
            $YMAKE install
         """,
        'version': '0.5.10.2',
        'meta': {
            'depends': ['libedit'],
        },
    }
