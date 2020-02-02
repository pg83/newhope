@y.package
def openssl0():
    version = '1.1.1c'

    if '{os}' == 'linux':
        flags = 'linux-x86_64-clang'
        extra = ['kernel-h']
    else:
        flags = 'darwin64-x86_64-cc'
        extra = []

    return {
        'code': """
            source fetch "https://www.openssl.org/source/old/{minver}/openssl-{version}.tar.gz" 1

            export CFLAGS=$(echo "$CFLAGS" | sed -e 's/isysroot/I/')

            $YPERL ./Configure {flags} no-asm threads no-shared no-dso no-hw no-tests no-engine --prefix=$IDIR --openssldir=$IDIR -w -std=c99 -D_GNU_SOURCE=1 $CFLAGS $LDFLAGS $LIBS
            $YMAKE -j $NTHRS
            $YMAKE install
        """.replace('{minver}', version[:-1]).replace('{flags}', flags),
        'version': version,
        'meta': {
            'kind': ['library'],
            'depends': extra + ['perl5','dl'],
            'provides': [
                {'lib': 'ssl', 'configure': {'opts': ['--with-openssl={pkgroot}', '--with-openssldir={pkgroot}']}},
                {'env': 'OPENSSL_INCLUDES', 'value': '{pkgroot}/include'},
            ],
        },
    }
