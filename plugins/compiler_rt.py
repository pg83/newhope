@y.package
def compiler_rt0():
    return {
        'code': """
             source fetch "http://releases.llvm.org/{version}/compiler-rt-{version}.src.tar.xz" 1
             source mk.sh
             mkdir $IDIR/lib && cp libcompiler_rt.a $IDIR/lib
        """,
        'extra': [
            {'kind': 'file', 'path': 'mk.sh', 'data': y.globals.by_name['data/mk_crt.sh']['data']},
        ],
        'version': '9.0.1',
        'meta': {
            'kind': ['library'],
            'provides': [
                {'lib': 'compiler_rt'},
            ],
        },
    }
