#if defined(__LINUX__)
    @y.package
    def toybox0():
        return {
            'code': '''
                mkdir -p $IDIR/bin
                cd $IDIR/bin
                source fetch "http://www.landley.net/toybox/downloads/binaries/{version}/toybox-{arch}" 0
                cp toybox-* toybox
                chmod +x toybox
            ''',
            'version': '0.8.1',
            'meta': {
                'kind': ['tool'],
                'undeps': ['make', 'musl'],
                'provides': [
                    {'env': 'TOYBOX', 'value': '{pkgroot}/bin/toybox'},
                ],
            },
        }
#endif
