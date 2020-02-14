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

            echo > empty.c
            $CC -c empty.c -o empty.o
            $AR q libdl.a empty.o

            export LDFLAGS="-L$(pwd) $LDFLAGS"

            export CXXFLAGS="$CFLAGS $CXXFLAGS"
            $YBASH ./Configure -des -Accflags="$CFLAGS" -Aldflags="$LDFLAGS $LIBS" -Dusethreads -Duse64bitall -Dprefix=$IDIR -Duseperlio -Uusesfio -Duseshrplib=false -Dusedl=false -Dcc="$CC -Duserelocatableinc $CFLAGS $LDFLAGS $LIBS" || true
            $YMAKE -j $NTHRS || $YMAKE -j $NTHRS  
            $YMAKE install
        """,
        'prepare': """
            source perl5_env
        """,
        'version': '5.30.1',
        'meta': {
            'kind': ['tool'],
            'depends': ['iconv', 'zlib', 'coreutils-boot', 'make', 'c', 'bash'],
            'provides': [
                {'env': 'YPERL', 'value': '{pkgroot}/bin/perl'},
                {'env': 'POD2HTML', 'value': '{pkgroot}/bin/pod2html'},
            ],
        },
    }
