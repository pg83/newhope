@y.package
def libpipeline0():
    return {
        'code': '''
            source fetch "http://download.savannah.nongnu.org/releases/libpipeline/libpipeline-{version}.tar.gz" 1
            $YSHELL ./configure $COFLAGS --enable-shared --disable-static --prefix=$IDIR || exit 1
            $YMAKE -j $THRS
            $YMAKE install
        ''',
        'version': '1.5.2',
        'meta': {
            'kind': ['library'],
            'provides': [
                {'lib': 'pipeline'},
                {'env': 'libpipeline_CFLAGS', 'value': '-I{pkgroot}i/include'},
                {'env': 'libpipeline_LiBS', 'value': '-L{pkgroot}i/libs -lpipeline'},
            ],
        }
    }