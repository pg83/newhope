@y.package
def make0():
    code = '''
        source fetch "http://mirror.lihnidos.org/GNU/ftp/gnu/make/make-{version}.tar.gz" 1
        export CFLAGS="-Dglob=make_glob -Dglobfree=make_globfree -Dfnmatch=make_fnmatch $CFLAGS"
        $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-load || exit 1
        $YMAKE -j $NTHRS
        $YMAKE install
    '''

    extra = []

    if '{os}' == 'linux':
        extra = ['musl-boot']

    return {
        'code': code,
        'meta': {
            'depends': ['make-boot'] + extra,
            'contains': ['make-boot'],
            'provides': [
                {'tool': 'YMAKE', 'value': '{pkgroot}/bin/make'},
            ],
        },
    }
