set +x

SRC=$(pwd)
ARCH="$1"
OPT="-std=c99 -nostdinc -ffreestanding -D_XOPEN_SOURCE=700"
CFLAGS="-O2 -w $OPT -I\$SRC/arch/$ARCH -I\$SRC/arch/generic -I\$SRC/src/include -I\$SRC/src/internal -I\$IDIR/include"
marker="\$IDIR/include/version.h"

echo "CFLAGS=\"$CFLAGS\""
echo ""

echo "$marker:"
cat << EOF | while read line; do echo "\t$line"; done
rm -rf "\$BDIR" "\$IDIR"
mkdir "\$BDIR" "\$BDIR/obj" "\$IDIR"
cp -R "\$SRC/include" "\$IDIR/"
cp -R "\$SRC/arch/generic/bits" "\$IDIR/include/"
cp -R "\$SRC/arch/$ARCH/bits" "\$IDIR/include/"
sed -f "\$SRC/tools/mkalltypes.sed" "\$SRC/arch/$ARCH/bits/alltypes.h.in" "\$SRC/include/alltypes.h.in" > "\$IDIR/include/bits/alltypes.h"
cp "\$SRC/arch/$ARCH/bits/syscall.h.in" "\$IDIR/include/bits/syscall.h"
sed -n -e s/__NR_/SYS_/p < "\$SRC/arch/$ARCH/bits/syscall.h.in" >> "\$IDIR/include/bits/syscall.h"
echo '#define VERSION "1.1.24"' > "\$IDIR/include/version.h"
EOF

echo ""

srcs=$(
    cd $SRC
    echo crt/crt1.c
    echo crt/dso.c
    
    for f in `ls src/ | grep -v include`; do
	ls src/$f/*.c
	ls src/$f/*.s
	ls src/$f/$ARCH/*.c
	ls src/$f/$ARCH/*.s
    done
) 2> /dev/null

outs=""
outs1=""

for s in $srcs; do
    b1=$(basename "$s")
    d1=$(dirname "$s")
    b2=$(basename "$d1")
    
    out1="${b2}_${b1}.o"
    outs1="$out1 $outs1"
    out="\$BDIR/obj/$out1"
    outs="$out $outs"
    
    echo "$out: \$SRC/$s $marker"
    echo "\t(\$CC \$CFLAGS -c \$2 -o \$1.tmp && mv \$1.tmp \$1) || exit 1"
    echo ""
done

arc="\$IDIR/lib/libc.a"

echo "$arc: $outs"
echo "\t(rm -rf \$IDIR/lib || true) && mkdir \$IDIR/lib"
echo "\tcd \$BDIR/obj && ar rc $arc $outs1"
echo "\tranlib $arc"
echo ""
echo "all: $arc $marker"
