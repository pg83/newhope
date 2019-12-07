@y.ygenerator()
def perl50():
    return {
        'code': """
            source fetch "https://www.cpan.org/src/5.0/perl-{version}.tar.gz" 1
            ./Configure -des -Accflags="$CFLAGS" -Aldflags="$LDFLAGS $LIBS" -Dusethreads -Duse64bitall -Dprefix=$IDIR -Duseperlio -Uusesfio -Duseshrplib=false -Dusedl=false
            $YMAKE -j4
            $YMAKE install
        """,
        'version': '5.30.1',
        'meta': {
            'kind': ['tool'],
            'depends': ['iconv', 'intl', 'zlib', 'coreutils'],
            'provides': [
                {'env': 'YPERL', 'value': '{pkgroot}/bin/perl'},
            ],
        },
    }
