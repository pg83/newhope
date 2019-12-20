env
$1 ./find_modules.py "$IDIR/lib/python$2" > all_modules.py
cat ./all_modules.py
$1 ../Tools/freeze/freeze.py ./all_modules.py
echo '#'"define Py_FrozenMain $4" >> frozen
cat frozen.c | grep -v 'extern int Py_' >> frozen
mv frozen frozen.c
$YMAKE OPT="$CFLAGS" -j $NTHRS
mv all_modules python
mkdir -p "$IDIR/bin"
install -v -m755 python "$IDIR/bin/staticpython$3"
