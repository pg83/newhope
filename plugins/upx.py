@y.package
def upx0():
    return {
        'code': '''
            source fetch "https://github.com/upx/upx/releases/download/v{version}/upx-{version}-amd64_linux.tar.xz" 1
            mkdir $IDIR/bin
            cp -p upx $IDIR/bin 
        ''',
        'meta': {
            'provides': [
                {'tool': 'YUPX', 'value': '"{pkgroot}/bin/upx"'},
            ],
            'repacks': {},
        },
    }
