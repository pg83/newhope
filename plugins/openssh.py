@y.package
def openssh0():
    return {
        'code': '''
            export CFLAGS="$OPENSSL_INCLUDES $CFLAGS"
            source fetch "https://cdn.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-{version}.tar.gz" 1
            $YSHELL ./configure $COFLAGS --prefix=/ --sysconfdir=/etc/ssh --enable-static --disable-shared --with-sandbox=no --without-hardening --without-rpath --with-shadow
            $YMAKE DESTDIR=$IDIR -j $NTHR
            $YMAKE DESTDIR=$IDIR install
        ''',
        'meta': {
            'kind': ['tool'],
            'depends': ['openssl', 'make', 'c', 'zlib', 'libedit'],
            'provides': [
                {'env': 'SSHD', 'value': '"{pkgroot}/sbin/sshd"'},
            ],
        },
    }
