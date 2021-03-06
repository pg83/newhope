@y.package
def tar0():
    return {
        'code': """
             source fetch "https://ftp.gnu.org/gnu/tar/tar-{version}.tar.gz" 1
             export FORCE_UNSAFE_CONFIGURE=1 
             $YSHELL ./configure $COFLAGS --prefix=$IDIR
             $YMAKE -j $NTHRS && $YMAKE install
        """,
        'meta': {
            'depends': ['iconv', 'intl', 'gzip', 'bzip2', 'xz', 'unrar', 'busybox-boot', 'make', 'c'],
            'provides': [
                {'tool': 'YGNUTAR', 'value': '{pkgroot}/bin/tar'},
            ],
        },
    }
