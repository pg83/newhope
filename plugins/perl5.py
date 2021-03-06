@y.package
def perl50():
    return {
        'code': """
            source fetch "https://www.cpan.org/src/5.0/perl-{version}.tar.gz" 0
            mv perl* xxx
            cd xxx

            source fake_binutils

            echo > empty.c
            $CC -c empty.c -o empty.o
            $AR q libdl.a empty.o

            export LDFLAGS="-L$(pwd) $LDFLAGS"
            export CXXFLAGS="$CFLAGS $CXXFLAGS"

            $YBASH  ./Configure -des -Accflags="$CFLAGS" -Aldflags="$LDFLAGS $LIBS" -Dusethreads -Duse64bitall -Dprefix=$IDIR -Duseperlio -Uusesfio -Duseshrplib=false -Dusedl=false -Dcc="$CC -Duserelocatableinc $CFLAGS $LDFLAGS $LIBS" || true
            $YMAKE -j $NTHRS || $YMAKE -j $NTHRS  
            $YMAKE install
        """,
        'prepare': """
            source perl5_env
        """,
        'meta': {
            'depends': ['iconv', 'zlib', 'coreutils-boot', 'make', 'c', 'bash'],
            'provides': [
                {'tool': 'YPERL', 'value': '{pkgroot}/bin/perl'},
                {'tool': 'POD2HTML', 'value': '{pkgroot}/bin/pod2html'},
            ],
        },
    }
