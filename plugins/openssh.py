@y.package
def openssh0():
    return {
        'code': '''
            export CFLAGS="$OPENSSL_INCLUDES $CFLAGS"
            source fetch "https://cdn.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-{version}.tar.gz" 1
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared
            $YMAKE -j $NTHR
            $YMAKE install
        ''',
        'meta': {
            'kind': ['tool'],
            'depends': ['openssl', 'make', 'c', 'zlib', 'jemalloc'],
            'provides': [
                {'env': 'SSHD', 'value': '"{pkgroot}/sbin/sshd"'},
            ],
        },
    }
