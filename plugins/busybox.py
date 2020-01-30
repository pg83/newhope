#if defined(__LINUX__)
    @y.package
    def busybox0():
        return {
            'os': 'linux',
            'code': """
                mkdir -p $IDIR/bin
                cd $IDIR/bin
                source fetch "https://www.busybox.net/downloads/binaries/{version}-defconfig-multiarch-musl/busybox-x86_64" 0
                mv busybox-* busybox
                chmod +x busybox
            """,
            'version': '1.31.0',
            'meta': {
                'kind': ['tool'],
                'provides': [
                    {'env': 'BUSYBOX', 'value': '{pkgroot}/bin/busybox'},
                ],
            },
        }
#endif
