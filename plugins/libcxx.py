@y.package
def libcxx0():
    if '{os}' == 'linux':
        sh = 'data/mk_libcxx.sh'
    else:
        sh = 'data/mk_libcxx_darwin.sh'

    return {
        'code': """
             #pragma cc
             source fetch "https://github.com/llvm/llvm-project/releases/download/llvmorg-{version}/libcxx-{version}.src.tar.xz" 0
             mv libcxx* xxx
             mv xxx/* ./
             $(F_0)
             $YSHELL mk.sh
        """,
        'extra': [
            {'kind': 'file', 'path': 'mk.sh', 'data': y.globals.by_name[sh]['data']},
        ],
        'meta': {
            'depends': ['libcxxrt', 'c'],
            'provides': [
                {'env': 'CPPFLAGS', 'value': '"-w -I/Library/Developer/CommandLineTools/SDKs/MacOSX10.15.sdk -I{pkgroot}/include"'},
                {'lib': 'c++'},
            ],
        },
    }
