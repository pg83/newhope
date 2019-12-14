set -e

rm -rf obj || true
mkdir obj

cxx_srcs=$(ls src/*.cc)
c_srcs=$(ls src/*.c)

for s in $cxx_srcs; do
    n=$(basename $s)
    $CXX $CFLAGS $CXXFLAGS -c $s -o obj/$n.o
done

for s in $c_srcs; do
    n=$(basename $s)
    $CC $CFLAGS -c $s -o obj/$n.o
done

$AR q obj/libcxxrt.a obj/*.o 
$RANLIB obj/libcxxrt.a

mkdir $IDIR/lib || true
mkdir $IDIR/include || true

cp obj/libcxxrt.a $IDIR/lib/
cp src/*.h $IDIR/include/
