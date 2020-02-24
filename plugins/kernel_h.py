if '{os}' == 'linux':
    @y.package
    def kernel_h0():
        return {
            'code': """
                source fetch "https://github.com/sabotage-linux/kernel-headers/archive/{version}.zip" 0
                mv kernel* xxx && cd xxx
                cd x86_64
                cp -RL ./include $IDIR/
            """,
            'meta': {
                'kind': ['library'],
                'provides': [
                    {'env': 'CPPFLAGS', 'value': '"$CPPFLAGS -I{pkgroot}/include"'},
                ],
            },
        }
