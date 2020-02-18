@y.package
def openssh():
    return {
        'code': '''
            source fetch "https://cdn.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-{version}.tar.gz" 1
            $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-static --disable-shared
            $YMAKE -j $NTHR
            $YMAKE install
        ''',
        'version': '8.2p1',
        'meta': {
            'kind': ['tool'],
            'depends': ['openssl', 'make', 'c', 'zlib'],
            'provides': [
                {'env': 'SSHD', 'value': '"{pkgroot}/sbin/sshd"'},
            ],
        },
    }
