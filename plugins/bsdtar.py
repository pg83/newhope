@y.package
def bsdtar0():
    return {
        'code': '''
             cp -R $(dirname $YTAR)/bin $IDIR/
             cf $IDIR/bin
             ln -s bsdtar tar
        ''',
        'meta': {
            'kind': ['tool'],
            'depends': ['libarchive'],
            'provides': [
                {'env': 'YTAR', 'value': '{pkgroot}/bin/bsdtar'},
            ]
        }
    }
