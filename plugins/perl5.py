@y.package
def perl50():
    return {
        'code': """
            source fetch "https://www.cpan.org/src/5.0/perl-{version}.tar.gz" 0
            mv perl* xxx
            cd xxx

            ln -s $AR ./ar
            ln -s $NM ./nm
            ln -s $CC ./gcc
            export PATH="$(pwd):$PATH"

            ./Configure -des -Accflags="$CFLAGS" -Aldflags="$LDFLAGS $LIBS" -Dusethreads -Duse64bitall -Dprefix=$IDIR -Duseperlio -Uusesfio -Duseshrplib=false -Dusedl=false -Dcc="$CC -Duserelocatableinc $CFLAGS $LDFLAGS $LIBS"
            $YMAKE -j $NTHRS
            $YMAKE install
        """,
        'prepare': """
            source perl5_env
        """,
        'version': '5.30.1',
        'meta': {
            'kind': ['tool'],
            'depends': ['iconv', 'zlib', 'coreutils-boot', 'dl'],
            'provides': [
                {'env': 'YPERL', 'value': '{pkgroot}/bin/perl'},
            ],
        },
    }
