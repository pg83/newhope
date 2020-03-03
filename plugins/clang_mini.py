@y.package
def clang_mini0():
    return {
        'code': '''
             mkdir $IDIR/bin
             cd $CLANG_ROOT/bin
             cp -pR clang clang++ clang-9 clang-cl clang-cpp ld64.lld ld.lld lld lld-link \
                    llvm-ar llvm-nm llvm-objcopy llvm-ranlib llvm-strip wasm-ld $IDIR/bin
        ''',
        'meta': {
            'depends': ['clang'],
            'provides': y.clang_provides(),
            'repacks': {},
        }
    }
