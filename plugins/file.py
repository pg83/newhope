@y.package
def file0():
    return {
        'code': """
             source fetch "ftp://ftp.astron.com/pub/file/file-{version}.tar.gz" 1
             $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'meta': {
            'kind': ['tool'],
            'depends': ['make', 'c'],
            'profides': [
                {'env': 'FILE_TOOL', 'value': '{pkgroot}/bin/file'}
            ],
        },
    }
