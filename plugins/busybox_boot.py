if '{os}' == 'linux':
    @y.package
    def busybox_boot0():
        return {
            'code': """
                mkdir -p $IDIR/bin
                cd $IDIR/bin
                source fetch "https://www.busybox.net/downloads/binaries/1.31.0-defconfig-multiarch-musl/busybox-{arch}" 0
                mv busybox-* busybox
                chmod +x busybox

                for x in `./busybox --list-full`; do
                    y=$(basename $x)
                    ln -fs busybox $y
                done
            """,
            'version': y.package_versions()['busybox'],
            'meta': {
                'provides': [
                    {'tool': 'BUSYBOX', 'value': '{pkgroot}/bin/busybox'},
                ],
                'repacks': {},
            },
        }
else:
    @y.package
    def busybox_boot0():
        return {
            'meta': {
                'kind': ['tool'],
            }
        }
