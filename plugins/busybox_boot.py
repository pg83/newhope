if '{os}' == 'linux':
    @y.package
    def busybox_boot0():
        return {
            'code': """
                mkdir -p $IDIR/bin
                cd $IDIR/bin
                source fetch "https://www.busybox.net/downloads/binaries/{version}-defconfig-multiarch-musl/busybox-{arch}" 0
                mv busybox-* busybox
                chmod +x busybox

                for x in `./busybox --list-full`; do
                    y=$(basename $x)
                    ln -fs busybox $y
                done
            """,
            'version': '1.31.1',
            'meta': {
                'kind': ['tool'],
                'undeps': ['make', 'musl', 'busybox-boot'],
                'provides': [
                    {'env': 'BUSYBOX', 'value': '{pkgroot}/bin/busybox'},
                ],
            },
        }
else:
    @y.package
    def busybox_boot0():
        return {
            'meta': {
                'kind': ['tool'],
                'undeps': ['busybox'],
            }
        }
