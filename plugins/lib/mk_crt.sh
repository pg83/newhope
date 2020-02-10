#!/bin/sh

set -e

(rm -rf b || true) && mkdir b && cd b

ls ../lib/builtins/ | grep udiv* | while read line
do
    ${CC} ${CFLAGS} -c "../lib/builtins/$line" -o $line.o
done

ls ../lib/builtins/ | grep umod* | while read line
do
    ${CC} ${CFLAGS} -c "../lib/builtins/$line" -o $line.o
done

${AR} q libcompiler_rt.a *.o

mv libcompiler_rt.a ..
cd ..
