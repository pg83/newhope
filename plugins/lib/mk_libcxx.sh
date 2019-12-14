set -e
set -x

DEFINES="
#if !defined(uiygfuiertyuiwetuyt)
#define uiygfuiertyuiwetuyt

#define _LIBCPP_HAS_MUSL_LIBC
#define _LIBCPP_HAS_MERGED_TYPEINFO_NAMES_DEFAULT 0

#endif
"

X_CXXFLAGS="-DNDEBUG -D_LIBCPP_BUILDING_LIBRARY -D_LIBCPP_HAS_COMMENT_LIB_PRAGMA -D_LIBCPP_HAS_NO_PRAGMA_SYSTEM_HEADER -iquote src  -I$IDIR/include -I$LIBCXXRT_INC -DLIBCXXRT -std=c++14 -nostdinc++ -fvisibility-inlines-hidden"

rm -rf obj || true
mkdir obj

echo "$DEFINES" > obj/__config
cat include/__config >> obj/__config

rm -rf $IDIR/include || true
mkdir $IDIR/include

rm -rf $IDIR/lib || true
mkdir $IDIR/lib

cp -R "include/"* $IDIR/include/
mv obj/__config $IDIR/include/

SRCS="
src/algorithm.cpp
src/any.cpp
src/bind.cpp
src/charconv.cpp
src/chrono.cpp
src/condition_variable.cpp
src/condition_variable_destructor.cpp
src/debug.cpp
src/exception.cpp
src/functional.cpp
src/future.cpp
src/hash.cpp
src/ios.cpp
src/iostream.cpp
src/locale.cpp
src/memory.cpp
src/mutex.cpp
src/mutex_destructor.cpp
src/new.cpp
src/optional.cpp
src/random.cpp
src/regex.cpp
src/shared_mutex.cpp
src/stdexcept.cpp
src/string.cpp
src/strstream.cpp
src/system_error.cpp
src/thread.cpp
src/typeinfo.cpp
src/utility.cpp
src/valarray.cpp
src/variant.cpp
src/vector.cpp
src/filesystem/operations.cpp
src/filesystem/directory_iterator.cpp
src/filesystem/int128_builtins.cpp
"

cat "src/filesystem/operations.cpp" | grep -v 'linux/version' | sed 's/LINUX_VERSION_CODE.*/1/' > qw
mv qw "src/filesystem/operations.cpp"

for s in $SRCS; do
    out=$(echo $s | tr '/' '_' | tr -d '\n').o
    $CXX $CXXFLAGS $X_CXXFLAGS -c $s -o obj/$out
done

$AR q obj/libc++.a "obj/"*.o
$RANLIB obj/libc++.a

mv obj/libc++.a $IDIR/lib/
