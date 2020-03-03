@y.package
def tcmalloc0():
    return {
        'code': '''
            source fetch "https://github.com/gperftools/gperftools/releases/download/gperftools-2.7/gperftools-2.7.tar.gz" 1

            echo > empty.c
            $CC -c empty.c -o empty.o
            $AR q libstdc++.a empty.o
            export LDFLAGS="-L$(pwd) $LDFLAGS" 
            export CFLAGS="$CFLAGS -D__USE_FILE_OFFSET64=1"

            $YSHELL ./configure $COFLAGS --prefix=$IDIR --enable-minimal --enable-static --disable-shared --disable-debugalloc --disable-heap-checker  --disable-heap-profiler --disable-cpu-profiler || exit 1

            echo '#define __off64_t long' > tmp
            cat ./src/malloc_hook_mmap_linux.h >> tmp
            mv tmp ./src/malloc_hook_mmap_linux.h

            echo '#undef __linux' > tmp
            cat ./src/malloc_hook.cc >> tmp
            mv tmp ./src/malloc_hook.cc

            $YMAKE -j $NTHRS
            $YMAKE install
        ''',
        'meta': {
            'depends': ['make', 'c', 'c++', 'kernel-h', 'libunwind'],
            'contains': ['mimalloc'],
            'provides': [
                {'lib': 'tcmalloc_minimal'},
            ],
        }
    }
