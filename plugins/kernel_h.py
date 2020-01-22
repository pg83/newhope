@y.ygenerator()
def kernel_h0():
    return {
        'os': 'linux',
        'code': """
             source fetch "https://github.com/sabotage-linux/kernel-headers/archive/{version}.zip" 0
             mv kernel* xxx && cd xxx
             cd x86_64
             cp -RL ./include $IDIR/
        """,
        'version': 'fefadd9e4e093f776cd14ee3685a80eb4ca000f4',
        'meta': {
            'kind': ['tool'],
            'provides': [
                {'env': 'CPPFLAGS', 'value': '"$CPPFLAGS -I{pkgroot}/include"'},
            ],
        },
    }
