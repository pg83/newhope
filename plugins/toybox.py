if '{os}' == 'linux':
    @y.package
    def toybox0():
        return {
            'code': '''
                mkdir -p $IDIR/bin
                cd $IDIR/bin
                source fetch "http://www.landley.net/toybox/downloads/binaries/{version}/toybox-{arch}" 0
                cp toybox-* toybox
                chmod +x toybox

                for i in `./toybox`; do
                    ln -fs toybox $i
                done
            ''',
            'version': '0.8.1',
            'meta': {
                'kind': ['tool'],
                'provides': [
                    {'env': 'TOYBOX', 'value': '{pkgroot}/bin/toybox'},
                ],
            },
        }
else:
    @y.package
    def toybox0():
        return {
            'meta': {
                'kind': ['tool']
            }
        }
