cd obj/src/malloc/
llvm-ar rc libmuslalloc.a *.lo
cp libmuslalloc.a $IDIR/lib
cd $IDIR/lib/
files=$(llvm-ar t libmuslalloc.a)
llvm-ar d libc.a $files
ranlib libc.a
