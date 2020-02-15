@y.package
def busybox0():
    return {
        'code': """
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
        'code1': """
            source fetch "https://www.busybox.net/downloads/busybox-{version}.tar.bz2" 1

            ln -s $CC ./gcc
            export PATH="$(pwd):$PATH"
            export CFLAGS="-Iinclude $CFLAGS"

            source no_free

            $YMAKE HOSTCFLAGS="$CFLAGS $LDFLAGS $LIBS" LDFLAGS="$LDFLAGS $LIBS" HOSTCXXFLAGS="$CXXFLAGS" HOSTLDFLAGS="$LDFLAGS $LIBS" defconfig

            cat include/ar.h | head -n 23 | tail -n 15 > tmp
            cat archival/libarchive/get_header_ar.c >> tmp
            cat tmp > archival/libarchive/get_header_ar.c 

            cat include/ar.h | head -n 23 | tail -n 15 > tmp
            cat archival/libarchive/unpack_ar_archive.c >> tmp
            cat tmp > archival/libarchive/unpack_ar_archive.c

            $YMAKE HOSTCFLAGS="$CFLAGS $LDFLAGS $LIBS" LDFLAGS="$LDFLAGS $LIBS" HOSTCXXFLAGS="$CXXFLAGS" HOSTLDFLAGS="$LDFLAGS $LIBS" -j $THRS
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
            'depends': ['make', 'kernel-h', 'make', 'c'],
            'provides': [
                {'env': 'BUSYBOX', 'value': '{pkgroot}/bin/busybox'},
            ],
            'contains': ['busybox-boot']
        },
    }
