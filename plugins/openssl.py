@y.ygenerator()
def openssl0():
    version = '1.1.1c'
        
    return {
        'code': """
            source fetch "https://www.openssl.org/source/old/{minver}/openssl-{version}.tar.gz" 1
            $YPERL ./Configure {flags} no-asm threads no-shared no-dso no-hw no-tests no-engine --prefix=$IDIR --openssldir=$IDIR -w -std=c99 -D_GNU_SOURCE=1 $CFLAGS $LDFLAGS $LIBS
            $YMAKE -j $NTHRS
            $YMAKE install
        """.replace('{minver}', version[:-1]),
        'extra': [
            {'os': 'linux', 'value': {'kind': 'subst', 'from': '{flags}', 'to': 'linux-x86_64-clang'}},
            {'os': 'darwin', 'value': {'kind': 'subst', 'from': '{flags}', 'to': 'darwin64-x86_64-cc'}},        
        ],
        'version': version,
        'meta': {
            'kind': ['library'],
            'depends': ['perl5', 'kernel-h', 'dl'],
            'provides': [
                {'lib': 'ssl'},
            ],
        },
    }
