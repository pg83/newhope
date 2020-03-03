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
            export CFLAGS="$(echo $CFLAGS | $SED -e 's/isysroot/I/')"
            export PATH="$(pwd):$PATH"
            $(F_0)
            $YPERL ./Configure {flags} no-asm threads no-shared no-dso no-hw no-tests no-engine --prefix=$IDIR --openssldir=$IDIR -w -std=c99 -D_GNU_SOURCE=1 $CFLAGS $LDFLAGS $LIBS || exit 1
            ($YMAKE -j $NTHRS) || ($YMAKE -j $NTHRS) || ($YMAKE -j $NTHRS)
            $YMAKE install
        """.replace('{minver}', version[:-1]).replace('{flags}', flags).replace('{version}', version),
        'extra': [
            {'kind': 'file', 'path': 'pod2html', 'data': y.builtin_data('data/pod2html')},
        ],
        'meta': {
            'depends': extra + ['perl5','dl', 'sed', 'busybox-boot', 'coreutils-boot', 'make', 'c'],
            'provides': [
                {'lib': 'ssl'},
                {'configure': '--with-openssl={pkgroot}'},
                {'configure': '--with-openssldir={pkgroot}'},
                {'configure': '--with-ssl-dir={pkgroot}'},
                {'env': 'OPENSSL_INCLUDES', 'value': '"-I{pkgroot}/include"'},
            ],
        },
    }
