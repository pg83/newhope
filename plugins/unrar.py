@ygenerator(tier=1, kind=['base', 'dev', 'tool'])
def unrar0(deps):
    return {
        'code': """
             $YMAKE -f makefile
             mkdir -p $IDIR/bin
             install -v -m755 unrar $IDIR/bin
        """,
        'url': 'http://www.rarlab.com/rar/unrarsrc-5.8.3.tar.gz',
        'deps': deps,
        'version': '5.8.3',
        'prepare': '$(ADD_PATH)',
    }
