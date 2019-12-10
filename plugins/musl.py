def musl_impl(code, deps):
    return {
        'os': 'linux',
        'code': code,
        'version': '1.1.24', 
        'extra': [
            {'kind': 'file', 'path': 'mk.sh', 'data': y.globals.by_name['data/build.sh']['data']},
        ],
        'meta': {
            'kind': ['library'],
            'depends': ['bestbox'] + deps,
            'provides': [
                {'lib': 'c'},
                {'env': 'CFLAGS', 'value': '"-nostdinc -isystem{pkgroot}/include $CFLAGS"'},
                {'env': 'LDFLAGS', 'value': '"-nostdlib -fuse-ld=lld -L{pkgroot}/lib $LDFLAGS"'},
                {'env': 'LIBS', 'value': '"{pkgroot}/lib/libc.a $LIBS"'},
                {'env': 'CC', 'value': '"/usr/bin/clang"'},
            ],
        },
    }


@y.ygenerator()
def musl_boot0():
    code = """
       source fetch "https://www.musl-libc.org/releases/musl-{version}.tar.gz" 1
       $(APPLY_EXTRA_PLAN_0)
       sh ./mk.sh x86_64 > Make.x86_64 && $SD/upm cmd pgmake -j4 -f ./Make.x86_64 --set SRC=$(pwd) --set BDIR=$BDIR/x --set IDIR=$IDIR --set CC=gcc '$IDIR/lib/libc.a'       
    """
    
    return musl_impl(code, [])

    
@y.ygenerator()
def musl0():
    code = """
       source fetch "https://www.musl-libc.org/releases/musl-{version}.tar.gz" 1
       $YSHELL ./configure --prefix=$IDIR --enable-static --disable-shared || exit 1
       $YMAKE -j3 || exit 1 
       $YMAKE install || exit 2
    """
    
    return musl_impl(code, ['make-boot'])
