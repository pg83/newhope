@y.package
def make0():
    code = '''
        source fetch "http://mirror.lihnidos.org/GNU/ftp/gnu/make/make-{version}.tar.gz" 1
        $YSHELL ./configure --prefix=$IDIR --disable-load || exit 1
        $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-load || exit 1
        $YMAKE -j $NTHRS
        $YMAKE install
    '''

    return {
        'code': code,
        'version': '4.2',
        'meta': {
            'kind': ['tool', 'box'],
            'depends': [
                'make-boot',
                #if defined(__LINUX__)
                    'musl-boot',
                #endif
            ],
            'undeps': ['make', 'musl'],
            'contains': ['make-boot'],
            'provides': [
                {'env': 'YMAKE', 'value': '{pkgroot}/bin/make'},
            ],
        },
    }
