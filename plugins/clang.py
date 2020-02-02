@y.package
def clang0():
    return {
        'code': '''
            source fetch "https://github.com/llvm/llvm-project/releases/download/llvmorg-{version}/llvm-project-{version}.tar.xz" 1
            mkdir build && cd build
            cmake -DCMAKE_C_COMPILER="$CC" -DCMAKE_CXX_COMPILER="$CXX" -DCMAKE_BUILD_TYPE=MinSizeRel -DLLVM_ENABLE_PROJECTS="clang;lld" -DBUILD_SHARED_LIBS=OFF LLVM_BUILD_LLVM_DYLIB=OFF ../llvm
        ''',
        'version': '9.0.1',
        'meta': {
            'depends': ['cmake', 'zlib', 'c++'],
            'kind': ['tool'], 
        },
    }
