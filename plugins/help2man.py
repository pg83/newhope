@y.package
def help2man0():
    return {
        'code': """
             source fetch "https://mirror.tochlab.net/pub/gnu/help2man/help2man-{version}.tar.xz" 1
             $YSHELL ./configure --prefix="$IDIR"
             $YMAKE -j $NTHRS
             $YMAKE install  
        """,
        'meta': {
            'depends': ['perl5', 'make', 'c'],
            'provides': [
                {'tool': 'HELP2MAN', 'value': '{pkgroot}/bin/help2man'},
            ],
        },
    }
