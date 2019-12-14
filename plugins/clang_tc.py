@y.ygenerator()
def clang_tc0():
    return {
        'meta': {
            'kind': ['library'],
            'provides': [
                {'env': 'CXX', 'value': '"/usr/bin/clang++"'},
                {'env': 'CXXFLAGS', 'value': '"-std=c++14 -nostdinc++ $CXXFLAGS"'},
                {'env': 'CC', 'value': '"/usr/bin/clang"'},
                {'env': 'CFLAGS', 'value': '"-nostdinc $CFLAGS"'},
                {'env': 'LDFLAGS', 'value': '"-nostdlib -static -fuse-ld=lld $LDFLAGS"'},
                {'env': 'RANLIB', 'value': '"/usr/bin/llvm-ranlib"'},
                {'env': 'AR', 'value': '"/usr/bin/llvm-ar"'},
            ],
        },
    }
