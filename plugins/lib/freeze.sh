#!/bin/sh

rm -rf *.c *.o Makefile >& /dev/null

P="$1"
PP=$(dirname "$P")
PH=$(dirname "$PP")
SP="$PH"/lib/$(basename "$P")

"$P" ./find_modules.py "$SP" > mods.py
"$P" "$PH/tools/freeze/freeze.py" "$2" ./mods.py
make -j
