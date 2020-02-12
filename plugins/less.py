@y.package
def less0():
    return {
        'code': """
             source fetch "http://www.greenwoodsoftware.com/less/less-{version}.tar.gz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'version': '551',
        'meta': {
            'kind': ['tool'],
            'profides': [
                {'env': 'LESS', 'value': '{pkgroot}/bin/less'}
            ],
        },
    }
