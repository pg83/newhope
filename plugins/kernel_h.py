@y.ygenerator()
def kernel_h0():
    return {
        'code': """
             source fetch "https://github.com/sabotage-linux/kernel-headers/archive/{version}.zip" 0
             mv kernel* xxx && cd xxx
             #$YMAKE ARCH=x86_64 prefix=/ DESTDIR=$IDIR install
             cd x86_64
             cp -RL ./include $IDIR/
        """,
        'version': 'fefadd9e4e093f776cd14ee3685a80eb4ca000f4',
        'meta': {
            'kind': ['library'],
        },
    }
