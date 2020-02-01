@y.package
def fetch_clang0():
    return {
        'code': '''
             cd $IDIR
             source fetch "https://github.com/llvm/llvm-project/releases/download/llvmorg-{version}/clang+llvm-{version}-{arch}-apple-{os}.tar.xz" 1
        ''',
        'version': '9.0.1',
        'meta': {
            'kind': ['tool', 'c', 'c++', 'linker', 'box'],
            'provides': [
                #{'env': 'CC', 'value': '"{pkgroot}/bin/clang"'},
                #{'env': 'CFLAGS', 'value': '"-nostdinc --target {os}-{arch} $CFLAGS"'},
                #{'env': 'AR', 'value': '"{pkgroot}/bin/llvm-ar"'},
                #{'env': 'RANLIB', 'value': '"{pkgroot}/bin/llvm-ranlib"'},
                #{'env': 'STRIP', 'value': '"{pkgroot}/bin/llvm-strip"'},
                #{'env': 'NM', 'value': '"{pkgroot}/bin/llvm-nm"'},
        #{'env': 'CXX', 'value': '"{pkgroot}/bin/clang++"'},
                #{'env': 'CXXFLAGS', 'value': '"-nostdinc++"'},
                #{'env': 'LD', 'value': '"{pkgroot}/bin/lld"'},
                #{'env': 'LDFLAGS', 'value': '"-nostdlib -static -all-static -fuse-ld=$LD"'},
            ],
        },
    }
