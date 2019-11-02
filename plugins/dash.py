@ygenerator(tier=2, kind=['core', 'dev', 'tool'])
def dash0(deps):
    return {
        'code': """
            ./configure --prefix=$IDIR
            $YMAKE -j2
            $YMAKE install
""",
        'src': 'http://gondor.apana.org.au/~herbert/dash/files/dash-0.5.10.2.tar.gz',
        'prepare': '$(ADD_PATH)',
        'deps': deps,
        'version': '0.5.10.2',
    }
