@y.package
def snv_client0():
    return {
        'code': '''
             mkdir "$IDIR/bin"
             cp -pR "$SVN" $IDIR/bin/
             $YUPX $IDIR/bin/*
        ''',
        'meta': {
            'kind': ['tool'],
            'depends': ['subversion', 'upx'],
            'repacks': {},
            'provides': [
                {'tool': 'SVN', 'value': '{pkgroot}/bin/svn'},
            ],
        },
    }
