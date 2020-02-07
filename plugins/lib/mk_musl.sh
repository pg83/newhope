set +x

SRC="$2"
ARCH="$1"
OPT="-std=c99 -nostdinc -ffreestanding -D_XOPEN_SOURCE=700 -fno-stack-protector -fomit-frame-pointer -fno-unwind-tables -fno-asynchronous-unwind-tables -ffunction-sections -fdata-sections"
CFLAGS="$PIC $OPT -I\$SRC/arch/$ARCH -I\$SRC/arch/generic -I\$SRC/src/include -I\$SRC/src/internal -I\$IDIR/include $CFLAGS"
marker="\$IDIR/include/version.h"

(
echo "set -x"
echo "export CFLAGS=\"$CFLAGS\""
echo ""
) > run.sh

cat << EOF >> run.sh
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

srcs=$(
    (cd $SRC
    
    ls crt/crt1.c
    ls crt/dso.c
    ls crt/$ARCH/*.c
    ls crt/$ARCH/*.s
    
    for f in `ls src/ | grep -v include`; do
	ls src/$f/*.c
	ls src/$f/*.s
	ls src/$f/$ARCH/*.c
	ls src/$f/$ARCH/*.s
    done) | grep -v 'dlsym.s'
) 2> /dev/null

outs=""
outs1=""

echo "set -x" > run1.sh
echo "set -x" > run2.sh
echo "set -x" > run3.sh
echo "set -x" > run4.sh
echo "set -x" > run5.sh
echo "set -x" > run6.sh
echo "set -x" > run7.sh
echo "set -x" > run8.sh

c=0

for s in $srcs; do
    b1=$(basename "$s")
    d1=$(dirname "$s")
    b2=$(basename "$d1")
    
    out1="${b2}_${b1}.o"
    outs1="$out1 $outs1"
    out="\$BDIR/obj/$out1"
    outs="$out $outs"

    c=$(((c + 1) % 8))
    f=$((c + 1))
    
    echo "(\$CC \$CFLAGS -c \$SRC/$s -o $out.tmp && mv $out.tmp $out) || exit 1" >> run$f.sh
done

arc="\$IDIR/lib/libc.a"

(
echo "sh run1.sh &"
echo "sh run2.sh &"
echo "sh run3.sh &"
echo "sh run4.sh &"
echo "sh run5.sh &"
echo "sh run6.sh &"
echo "sh run7.sh &"
echo "sh run8.sh &"
echo "wait"
echo "(rm -rf \$IDIR/lib || true) && mkdir \$IDIR/lib"
echo "cd \$BDIR/obj && \$AR rc $arc $outs1"
echo "\$RANLIB $arc"
) >> run.sh
