@y.package
def busybox0():
    return {
        'code1': """
            mkdir -p $IDIR/bin
            cd $IDIR/bin
            source fetch "https://www.busybox.net/downloads/binaries/{version}-defconfig-multiarch-musl/busybox-{arch}" 0
            mv busybox-* busybox
            chmod +x busybox

            for x in `./busybox --list-full`; do
                y=$(basename $x)
                ln -fs busybox $y
            done
        """,
        'code': """
            source fetch "https://www.busybox.net/downloads/busybox-{version}.tar.bz2" 1

            ln -s $CC ./gcc
            export PATH="$(pwd):$PATH"
            export CFLAGS="-Iinclude $CFLAGS"
            export LIBS="$LIBS -Wl,--whole-archive"

            $YMAKE HOSTCFLAGS="$CFLAGS $LDFLAGS $LIBS" LDFLAGS="$LDFLAGS $LIBS" HOSTCXXFLAGS="$CXXFLAGS" HOSTLDFLAGS="$LDFLAGS $LIBS" defconfig

            cat include/ar.h | head -n 23 | tail -n 15 > tmp
            cat archival/libarchive/get_header_ar.c >> tmp
            cat tmp > archival/libarchive/get_header_ar.c 

            cat include/ar.h | head -n 23 | tail -n 15 > tmp
            cat archival/libarchive/unpack_ar_archive.c >> tmp
            cat tmp > archival/libarchive/unpack_ar_archive.c

            $YMAKE HOSTCFLAGS="$CFLAGS $LDFLAGS $LIBS" LDFLAGS="$LDFLAGS $LIBS" HOSTCXXFLAGS="$CXXFLAGS" HOSTLDFLAGS="$LDFLAGS $LIBS" V=1 -j $THRS || exit 1
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
            unlink vi
        """,
        'meta': {
            'kind': ['tool'],
            'depends': ['make', 'kernel-h', 'make', 'c'],
            'provides': [
                {'env': 'BUSYBOX', 'value': '{pkgroot}/bin/busybox'},
            ],
            'contains': ['busybox-boot']
        },
    }
