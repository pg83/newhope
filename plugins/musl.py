#if defined(__LINUX__)

def musl_impl(code, deps, cont, kind):
    return {
        'os': 'linux',
        'code': code,
        'version': '1.1.24', 
        'extra': [
            {'kind': 'file', 'path': 'mk.sh', 'data': y.globals.by_name['data/mk_musl.sh']['data']},
            {'kind': 'file', 'path': 'crt/dso.c', 'data': y.globals.by_name['data/dso.c']['data']},
            {'kind': 'file', 'path': 'malloc.sh', 'data': y.globals.by_name['data/malloc.sh']['data']},
        ],
        'meta': {
            'kind': kind,
            'contains': cont,
            'depends': ['bestbox'] + deps,
            'provides': [
                {'lib': 'muslc'},
                {'env': 'CPPFLAGS', 'value': '"$CPPFLAGS -I{pkgroot}/include"'},
                {'env': 'CFLAGS', 'value': '"-w $CFLAGS"'},
            ],
        },
    }


@y.ygenerator()
def musl_boot0():
    code = """
       source fetch "https://www.musl-libc.org/releases/musl-{version}.tar.gz" 1
       $(APPLY_EXTRA_PLAN_0)
       $(APPLY_EXTRA_PLAN_1)
       export CFLAGS="-Diconv=musl_iconv -Diconv_open=musl_iconv_open -Diconv_close=musl_iconv_close $CFLAGS"
       sh ./mk.sh x86_64 .
       SRC=$(pwd) BDIR=$BDIR/build IDIR=$IDIR CC=$CC sh run.sh
       (cd $IDIR/lib && ln -s libc.a libmuslc.a)
       rm $IDIR/include/iconv.h
       source fetch_url "$IDIR/include/stdatomic.h" "https://raw.githubusercontent.com/llvm-mirror/clang/master/lib/Headers/stdatomic.h"
    """

    return musl_impl(code, [], [], ['tool'])


@y.ygenerator()
def musl0():
    code = """
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
    """

    res = y.dc(musl_impl(code, ['make-boot', 'mimalloc'], ['musl-boot'], ['library']))

    return res

#endif
