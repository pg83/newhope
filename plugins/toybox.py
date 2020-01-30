#if defined(__LINUX__)
    @y.package
    def toybox0():
        return {
            'os': 'linux',
            'code': '''
                mkdir -p $IDIR/bin
                cd $IDIR/bin
                source fetch "http://www.landley.net/toybox/downloads/binaries/{version}/toybox-x86_64" 0
                cp toybox-* toybox
                chmod +x toybox
            ''',
            'version': '0.8.1',
            'meta': {
                'kind': ['tool'],
                'provides': [
                    {'env': 'TOYBOX', 'value': '{pkgroot}/bin/toybox'},
                ],
            },
        }
#endif
