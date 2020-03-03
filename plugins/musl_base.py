if '{os}' == 'linux':
    @y.package
    def musl_base0():
        return {
            'code': """
                source fetch "https://www.musl-libc.org/releases/musl-{version}.tar.gz" 1
                export CFLAGS="-Diconv=musl_iconv -Diconv_open=musl_iconv_open -Diconv_close=musl_iconv_close -Ddlopen=musl_dlopen -Ddlclose=musl_dlclose -Ddlerror=musl_dlerror -Ddlsym=musl_dlsym $CFLAGS"
                rm src/ldso/x86_64/dlsym.s
                $YSHELL ./configure --prefix=$IDIR --enable-static --disable-shared || exit 1
                $(F_3)
                mv crt1.c crt/
                $YMAKE -j $NTHRS || exit 1
                $YMAKE install || exit 2
                $(F_2)
                source ./malloc.sh
                (cd $IDIR/lib && $AR q libc.a crt1.o crti.o crtn.o && rm *crt* && $RANLIB libc.a && ln -s libc.a libmuslc.a && rm libdl.a)
                rm $IDIR/include/iconv.h
                source fetch_url "$IDIR/include/stdatomic.h" "https://raw.githubusercontent.com/llvm-mirror/clang/master/lib/Headers/stdatomic.h"
                echo '#include <sys/sysmacros.h>' > "$IDIR/include/sys/mkdev.h"
            """,
            'version': y.package_versions()['musl'],
            'extra': [
                {'kind': 'file', 'path': 'mk.sh', 'data': y.globals.by_name['data/mk_musl.sh']['data']},
                {'kind': 'file', 'path': 'crt/dso.c', 'data': y.globals.by_name['data/dso.c']['data']},
                {'kind': 'file', 'path': 'malloc.sh', 'data': y.globals.by_name['data/malloc.sh']['data']},
                {'kind': 'file', 'path': 'crt1.c', 'data': y.globals.by_name['data/crt1.c']['data']},
            ],
            'meta': {
                'depends': ['busybox-boot', 'make-boot'],
                'provides': [
                    {'tool': 'MUSL_ROOT', 'value': '"{pkgroot}"'},
                ],
                'repacks': {},
            },
        }

