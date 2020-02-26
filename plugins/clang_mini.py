@y.package
def clang_mini0():
    return {
        'code': '''
             mkdir $IDIR/bin
             cd $(dirname "$CLANG")
             cp -pR clang clang++ clang-9 clang-cl clang-cpp ld64.lld ld.lld lld lld-link \
                    llvm-ar llvm-nm llvm-objcopy llvm-ranlib llvm-strip wasm-ld $IDIR/bin
        ''',
        'meta': {
            'kind': ['tool'],
            'depends': ['clang'],
            'provides': y.clang_provides(),
        }
    }
