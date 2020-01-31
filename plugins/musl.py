#if defined(__LINUX__)
    @y.package
    def musl0():
        return {
            'code': """
                source fetch "https://www.musl-libc.org/releases/musl-{version}.tar.gz" 1
                export CFLAGS="-Diconv=musl_iconv -Diconv_open=musl_iconv_open -Diconv_close=musl_iconv_close -Ddlopen=musl_dlopen -Ddlclose=musl_dlclose -Ddlerror=musl_dlerror -Ddlsym=musl_dlsym $CFLAGS"
                rm src/ldso/x86_64/dlsym.s
                $YSHELL ./configure --prefix=$IDIR --enable-static --disable-shared || exit 1
                $YMAKE -j $NTHRS || exit 1
                $YMAKE install || exit 2
                $(APPLY_EXTRA_PLAN_2)
                source ./malloc.sh
                (cd $IDIR/lib && $AR q libc.a crt1.o crti.o crtn.o && rm *crt* && $RANLIB libc.a && ln -s libc.a libmuslc.a && rm libdl.a)
                rm $IDIR/include/iconv.h
                source fetch_url "$IDIR/include/stdatomic.h" "https://raw.githubusercontent.com/llvm-mirror/clang/master/lib/Headers/stdatomic.h"
            """,
            'version': '1.1.24', 
            'extra': [
                {'kind': 'file', 'path': 'mk.sh', 'data': y.globals.by_name['data/mk_musl.sh']['data']},
                {'kind': 'file', 'path': 'crt/dso.c', 'data': y.globals.by_name['data/dso.c']['data']},
                {'kind': 'file', 'path': 'malloc.sh', 'data': y.globals.by_name['data/malloc.sh']['data']},
            ],
            'meta': {
                'kind': ['library'],
                'contains': ['musl-boot'],
                'depends': ['bestbox', 'make-boot', 'mimalloc'],
                'undeps': ['make', 'musl'],
                'provides': [
                    {'lib': 'muslc'},
                    {'env': 'CPPFLAGS', 'value': '"$CPPFLAGS -I{pkgroot}/include"'},
                    {'env': 'CFLAGS', 'value': '"-w $CFLAGS"'},
                ],
            },
        }
#endif
