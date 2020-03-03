@y.package
def snv_server0():
    return {
        'code': '''
             mkdir "$IDIR/bin"
             cd "$IDIR/bin"
             cp -pR $(dirname "$SVN")/* ./
             rm svn
             $YUPX ./*
        ''',
        'meta': {
            'depends': ['subversion', 'upx'],
            'repacks': {},
        },
    }
