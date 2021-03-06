
set -e
set -x

COMMON="-I./src -I./include -D_LIBUNWIND_HAS_COMMENT_LIB_PRAGMA -funwind-tables -nostdinc++ -D_DEBUG -D_LIBUNWIND_IS_NATIVE_ONLY"
CXXFLAGS="$COMMON -std=c++11 -fstrict-aliasing -fno-exceptions -fno-rtti $CXXFLAGS"
CFLAGS="$COMMON -std=c99 $CFLAGS"

rm -rf obj || true
mkdir obj

cxx_src="
src/libunwind.cpp
src/Unwind-EHABI.cpp
src/Unwind-seh.cpp
src/Unwind_AppleExtras.cpp
"

cc_srcs="
src/UnwindLevel1.c
src/UnwindLevel1-gcc-ext.c
src/Unwind-sjlj.c
"

asm_srcs="
src/UnwindRegistersRestore.S
src/UnwindRegistersSave.S
unwind.c
"

echo 'extern *void_ZN9libunwind15Registers_arm646jumptoEv;' >> unwind.c

for s in $cxx_src; do
    $CXX $CXXFLAGS -c $s -o obj/$(basename $s).o
done

for s in $cc_srcs $asm_srcs; do
    $CC $CFLAGS -c $s -o obj/$(basename $s).o
done

$AR q obj/libunwind.a obj/*.o
$RANLIB obj/libunwind.a

mkdir $IDIR/lib
cp obj/libunwind.a $IDIR/lib
cp -R include $IDIR/
