if '{os}' == 'linux':
    @y.package
    def musl_boot0():
        return {
            'code': '''
                source fetch "https://www.musl-libc.org/releases/musl-{version}.tar.gz" 1
                $(APPLY_EXTRA_PLAN_0)
                $(APPLY_EXTRA_PLAN_1)
                export CFLAGS="-Diconv=musl_iconv -Diconv_open=musl_iconv_open -Diconv_close=musl_iconv_close $CFLAGS"
                sh ./mk.sh x86_64 .
                SRC=$(pwd) BDIR=$BDIR/build IDIR=$IDIR CC=$CC sh run.sh
                (cd $IDIR/lib && ln -s libc.a libmuslc.a)
                rm $IDIR/include/iconv.h
                source fetch_url "$IDIR/include/stdatomic.h" "https://raw.githubusercontent.com/llvm-mirror/clang/master/lib/Headers/stdatomic.h"
            ''',
            'version': '1.1.24', 
            'extra': [
                {'kind': 'file', 'path': 'mk.sh', 'data': y.globals.by_name['data/mk_musl.sh']['data']},
                {'kind': 'file', 'path': 'crt/dso.c', 'data': y.globals.by_name['data/dso.c']['data']},
                {'kind': 'file', 'path': 'malloc.sh', 'data': y.globals.by_name['data/malloc.sh']['data']},
            ],
            'meta': {
            'kind': ['tool'],
                'depends': ['busybox-boot', 'toybox'],
                'undeps': ['musl', 'make'],
                'provides': [
                    {'lib': 'muslc'},
                    {'env': 'CPPFLAGS', 'value': '"$CPPFLAGS -I{pkgroot}/include"'},
                    {'env': 'CFLAGS', 'value': '"-w $CFLAGS"'},
                ],
            },
        }
