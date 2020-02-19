@y.package
def ucl0():
    return {
        'code': '''
            source fetch "http://www.oberhumer.com/opensource/ucl/download/ucl-{version}.tar.gz" 1
            export UCL_CFLAGS="$CFLAGS"
            $YSHELL ./configure --prefix=$IDIR --disable-shared --enable-static --without-pic
            $YMAKE -j $NTHR
            $YMAKE install
        ''',
        'version': '1.03',
        'meta': {
            'kind': ['library'],
            'depends': ['musl', 'c'],
            'provides': [
                {'lib': 'ucl'},
                {'env': 'UPX_UCLDIR', 'value': '"{pkgroot}"'},
            ]
        },
    }
