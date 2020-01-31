#@y.package
def generic_clang0():
    return {
        'code': '''
             cd $IDIR
             source fetch "https://github.com/llvm/llvm-project/releases/download/llvmorg-{version}/clang+llvm-{version}-{arch}-apple-{os}.tar.xz" "1"
        ''',
        'version': '9.0.1',
        'meta': {
            'kind': ['tool', 'c', 'c++', 'linker'],
            'provides': {}
        }
    }
