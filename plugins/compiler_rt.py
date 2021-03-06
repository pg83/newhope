@y.package
def crt0():
    return {
        'code': """
             #pragma cc
             source fetch "https://github.com/llvm/llvm-project/releases/download/llvmorg-{version}/compiler-rt-{version}.src.tar.xz" 1
             $(F_0)
             source mk.sh
             mkdir $IDIR/lib && cp libcompiler_rt.a $IDIR/lib
        """,
        'extra': [
            {'kind': 'file', 'path': 'mk.sh', 'data': y.globals.by_name['data/mk_crt.sh']['data']},
        ],
        'meta': {
            'depends': ['make', 'c'],
            'provides': [
                {'lib': 'compiler_rt'},
            ],
        },
    }
