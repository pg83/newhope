#@y.package
def clang0():
    return {
        'code': '''
            source fetch "https://github.com/llvm/llvm-project/releases/download/llvmorg-{version}/llvm-project-{version}.tar.xz" 1
            mkdir build && cd build
            export CXXFLAGS="-U__SSE2__ $CXXFLAGS"
            cmake -DCMAKE_INSTALL_PREFIX=$IDIR -DCMAKE_EXE_LINKER_FLAGS="$LDFLAGS $LIBS" -DCMAKE_C_COMPILER="$CC" -DCMAKE_CXX_COMPILER="$CXX" -DCMAKE_BUILD_TYPE=MinSizeRel -DCMAKE_C_FLAGS_MINSIZEREL="$CFLAGS $LDFLAGS $LIBS" -DCMAKE_CXX_FLAGS_MINSIZEREL="$CXXFLAGS $LDFLAGS $LIBS" -DLLVM_ENABLE_PROJECTS="clang;lld" -DBUILD_SHARED_LIBS=OFF LLVM_BUILD_LLVM_DYLIB=OFF -DLLVM_PTHREAD_LIB='-lmuslc' ../llvm
            $YMAKE -j 7 -k || true
            cp -pR bin $IDIR/
        ''',
        'meta': {
            'depends': ['cmake', 'zlib', 'c++', 'make', 'c'],
            'kind': ['tool'], 
        },
    }
