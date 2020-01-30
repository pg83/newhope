@y.package
def slibtool0():
    return {
        'code': """
             source fetch "https://git.foss21.org/slibtool/snapshot/slibtool-{version}.tar.xz" 1
             $YSHELL ./configure --prefix=$IDIR || exit1 
             $YMAKE -j $NTHRS install || exit 1
        """,
        'version': '0.5.28',
        'meta': {
            'kind': ['tool', 'box'],
            'provides': [
                {'env': 'LIBTOOL', 'value': 'export LIBTOOL="{pkgroot}/bin/dlibtool"'},
            ],
        },
    }
