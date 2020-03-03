@y.package
def make_boot0():
    extra = []

    if '{os}' == 'linux':
        extra = ['musl-boot', 'busybox-boot']

    code = '''
        source fetch "http://mirror.lihnidos.org/GNU/ftp/gnu/make/make-{version}.tar.gz" 1
        export CPPFLAGS="-I./glob -Dglob=make_glob -Dglobfree=make_globfree -Dfnmatch=make_fnmatch $CPPFLAGS"
        $YSHELL ./configure --prefix=$IDIR --disable-load || exit 1
        $YSHELL ./build.sh
        mkdir $IDIR/bin && cp make $IDIR/bin/ && chmod +x $IDIR/bin/make
    '''

    return {
        'code': code,
        'version': y.package_versions()['make'],
        'meta': {
            'depends': extra,
            'provides': [
                {'tool': 'YMAKE', 'value': '{pkgroot}/bin/make'},
            ],
        },
    }
