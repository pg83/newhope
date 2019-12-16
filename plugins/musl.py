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
                {'env': 'CFLAGS', 'value': '"-isystem{pkgroot}/include $CFLAGS"'},
            ],
        },
    }


@y.ygenerator()
def musl_boot0():
    code = """
       source fetch "https://www.musl-libc.org/releases/musl-{version}.tar.gz" 1
       $(APPLY_EXTRA_PLAN_0)
       $(APPLY_EXTRA_PLAN_1)
       sh ./mk.sh x86_64 .
       SRC=$(pwd) BDIR=$BDIR/build IDIR=$IDIR CC=/usr/bin/gcc sh run.sh
       cd $IDIR/lib
       ln -s libc.a libmuslc.a
    """
    
    return musl_impl(code, [], [], ['tool'])

    
@y.ygenerator()
def musl0():
    code = """
       source fetch "https://www.musl-libc.org/releases/musl-{version}.tar.gz" 1
       $YSHELL ./configure --prefix=$IDIR --enable-static --disable-shared || exit 1
       $YMAKE -j $NTHRS || exit 1 
       $YMAKE install || exit 2
       $(APPLY_EXTRA_PLAN_2)
       source ./malloc.sh
       cd $IDIR/lib
       $AR q libc.a crt1.o crti.o crtn.o
       rm *crt*
       $RANLIB libc.a
       ln -s libc.a libmuslc.a
    """
    
    res = y.deep_copy(musl_impl(code, ['make-boot', 'jemalloc'], ['musl-boot'], ['library']))

    return res
