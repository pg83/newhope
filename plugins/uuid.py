@y.package
def uuid_dev0():
    return {
        'code': '''
             mkdir $IDIR/lib $IDIR/include
             cp -pR $UL_ROOT/lib/libuuid.a $IDIR/lib/
             cp -pR $UL_ROOT/include/uuid $IDIR/include/
        ''',
        'meta': {
            'kind': ['library'],
            'depends': ['util-linux'],
            'provides': [
                {'lib': 'uuid'},
            ],
            'repacks': {},
        },
    }
