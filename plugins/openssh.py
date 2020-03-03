@y.package
def openssh0():
    return {
        'code': '''
            export CFLAGS="$OPENSSL_INCLUDES $CFLAGS"
            source fetch "https://cdn.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-{version}.tar.gz" 1
            $YSHELL ./configure $COFLAGS --prefix=/ --sysconfdir=/etc/ssh --enable-static --disable-shared --with-sandbox=no --without-hardening --with-shadow
            $YMAKE DESTDIR=$IDIR -j $NTHR
            $YMAKE DESTDIR=$IDIR install
        ''',
        'meta': {
            'depends': ['openssl', 'make', 'c', 'zlib', 'libedit', 'jemalloc'],
            'provides': [
                {'tool': 'SSHD', 'value': '"{pkgroot}/sbin/sshd"'},
            ],
            'repacks': {},
        },
    }
