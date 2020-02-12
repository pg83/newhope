@y.package
def busybox0():
    return {
        'code': """
            source fetch "https://www.busybox.net/downloads/busybox-{version}.tar.bz2" 1

            ln -s $CC ./gcc
            export PATH="$(pwd):$PATH"
            export CFLAGS="-Iinclude $CFLAGS"

            $YMAKE HOSTCFLAGS="$CFLAGS $LDFLAGS $LIBS" LDFLAGS="$LDFLAGS $LIBS" HOSTCXXFLAGS="$CXXFLAGS" HOSTLDFLAGS="$LDFLAGS $LIBS" defconfig

            cat include/ar.h | head -n 23 | tail -n 15 > tmp
            cat archival/libarchive/get_header_ar.c >> tmp
            cat tmp > archival/libarchive/get_header_ar.c 

            cat include/ar.h | head -n 23 | tail -n 15 > tmp
            cat archival/libarchive/unpack_ar_archive.c >> tmp
            cat tmp > archival/libarchive/unpack_ar_archive.c

            $YMAKE HOSTCFLAGS="$CFLAGS $LDFLAGS $LIBS" LDFLAGS="$LDFLAGS $LIBS" HOSTCXXFLAGS="$CXXFLAGS" HOSTLDFLAGS="$LDFLAGS $LIBS" -j $THRS

            #$CC $LDFLAGS applets/built-in.o archival/lib.a  archival/libarchive/lib.a  console-tools/lib.a  coreutils/lib.a  coreutils/libcoreutils/lib.a  debianutils/lib.a  klibc-utils/lib.a  e2fsprogs/lib.a  editors/lib.a  findutils/lib.a  init/lib.a  libbb/lib.a  libpwdgrp/lib.a  loginutils/lib.a  mailutils/lib.a  miscutils/lib.a  modutils/lib.a  networking/lib.a  networking/libiproute/lib.a  networking/udhcp/lib.a  printutils/lib.a  procps/lib.a  runit/lib.a  selinux/lib.a  shell/lib.a  sysklogd/lib.a  util-linux/lib.a  util-linux/volume_id/lib.a  archival/built-in.o  archival/libarchive/built-in.o  console-tools/built-in.o  coreutils/built-in.o  coreutils/libcoreutils/built-in.o  debianutils/built-in.o  klibc-utils/built-in.o  e2fsprogs/built-in.o  editors/built-in.o  findutils/built-in.o  init/built-in.o  libbb/built-in.o  libpwdgrp/built-in.o  loginutils/built-in.o  mailutils/built-in.o  miscutils/built-in.o  modutils/built-in.o  networking/built-in.o  networking/libiproute/built-in.o  networking/udhcp/built-in.o  printutils/built-in.o  procps/built-in.o  runit/built-in.o  selinux/built-in.o  shell/built-in.o  sysklogd/built-in.o  util-linux/built-in.o  util-linux/volume_id/built-in.o -lmuslc -lmimalloc -lmuslc -ljemalloc -o busybox

            mkdir $IDIR/bin && cp busybox $IDIR/bin && cd $IDIR/bin
            chmod +x busybox

            for x in `./busybox --list-full`; do
                y=$(basename $x)
                ln -fs busybox $y
            done

            unlink ash
            unlink bc 
            unlink awk
            unlink sh
            unlink wget
        """,
        'version': '1.31.1',
        'meta': {
            'kind': ['tool'],
            'depends': ['make', 'kernel-h'],
            'provides': [
                {'env': 'BUSYBOX', 'value': '{pkgroot}/bin/busybox'},
            ],
            'contains': ['busybox-boot']
        },
    }
