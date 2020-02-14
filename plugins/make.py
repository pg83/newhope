@y.package
def make0():
    code = '''
        source fetch "http://mirror.lihnidos.org/GNU/ftp/gnu/make/make-{version}.tar.gz" 1
        $YSHELL ./configure --prefix=$IDIR --disable-load || exit 1
        $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-load || exit 1
        $YMAKE -j $NTHRS
        $YMAKE install
    '''

    extra = []

    if '{os}' == 'linux':
        extra = ['musl-boot']

    return {
        'code': code,
        'version': '4.2',
        'meta': {
            'kind': ['box'],
            'depends': ['make-boot'] + extra,
            'contains': ['make-boot'],
            'provides': [
                {'env': 'YMAKE', 'value': '{pkgroot}/bin/make'},
            ],
        },
    }
