cd obj/src/malloc/
$AR rc libmuslalloc.a *.lo
cp libmuslalloc.a $IDIR/lib
cd $IDIR/lib/
files=$($AR t libmuslalloc.a)
$AR d libc.a $files
$RANLIB libc.a
