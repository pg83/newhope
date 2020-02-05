@y.package
def bsdtar0():
    return {
        'code': '''
             mkdir "$IDIR/bin"
             cp "$YBSDTAR" "$IDIR/bin"
             cd "$IDIR/bin"
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
