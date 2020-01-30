@y.package
def make0():
    def it():
        yield 'source fetch "http://mirror.lihnidos.org/GNU/ftp/gnu/make/make-{version}.tar.gz" 1'
        yield '$YSHELL ./configure --prefix=$IDIR --disable-load || exit 1'
        yield '$YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-load || exit 1'
        yield '$YMAKE -j $NTHRS'
        yield '$YMAKE install'

    return {
        'code': '\n'.join(it()),
        'version': '4.2',
        'meta': {
            'kind': ['tool', 'box'],
            'depends': ['make-boot'],
            'contains': ['make-boot'],
            'provides': [
                {'env': 'YMAKE', 'value': '{pkgroot}/bin/make'},
            ],
        },
    }
