@y.package
def util_linux0():
    return {
        'code': '''
            source fetch "https://mirrors.edge.kernel.org/pub/linux/utils/util-linux/v2.35/util-linux-{version}.tar.xz" 1

            echo > empty.c
            $CC -c empty.c -o empty.o
            $AR q libdl.a empty.o
            cp libdl.a libtinfo.a
            export LDFLAGS="-L$(pwd) $LDFLAGS"

            $YSHELL ./configure --prefix=$IDIR --disable-shared --enable-static --without-pic --without-systemd --without-selinux --without-python --without-tinfo --with-slang --disable-more --disable-makeinstall-chown --disable-makeinstall-setuid --with-bashcompletiondir=$IDIR/share/bash
            $YMAKE -j $NTHR
            $YMAKE install

            ($YUPX $IDIR/bin/*) || true
            ($YUPX $IDIR/sbin/*) || true
        ''',
        'meta': {
            'kind': ['tool'],
            'depends': ['upx', 'slang', 'readline', 'ncurses', 'musl', 'c', 'kernel-h', 'iconv', 'intl'],
        },
    }
