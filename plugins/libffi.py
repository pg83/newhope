@y.package
def libffi0():
    return {
        'code': """
             source fetch "https://sourceware.org/ftp/libffi/libffi-{version}.tar.gz" 1

             $SED -e '/^includesdir/ s/$(libdir).*$/$(includedir)/' \
                  -i include/Makefile.in

             $SED -e '/^includedir/ s/=.*$/=@includedir@/' \
                  -e 's/^Cflags: -I${includedir}/Cflags:/' \
                  -i libffi.pc.in

             $YSHELL ./configure $COFLAGS --prefix=$IDIR --disable-shared --enable-static || exit 1
             $YMAKE -j $NTHRS
             $YMAKE install
        """,
        'version': '3.2.1',
        'meta': {
            'kind': ['library'],
            'depends': ['sed'],
            'provides': [
                {'lib': 'ffi'},
                {'env': 'LIBFFI_CFLAGS', 'value': '-I/{pkgroot}/include'},
            ],
        },
    }
