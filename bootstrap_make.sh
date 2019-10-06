wget http://ftp.gnu.org/gnu/make/make-4.2.1.tar.bz2

mkdir 1
cd 1
cat ../make-4.2.1.tar.bz2 | tar -xjf -
cd make-4.2.1
export LDFLAGS='--static'
export PATH=/cross_tools/x86_64-linux-musl-native/bin:$PATH
./configure --prefix=/
./build.sh
/bin/sh
./make
cp ./make /bin

cd /build

mkdir 2
cd 2
cat ../make-4.2.1.tar.bz2 | tar -xjf -
cd make-4.2.1
export LDFLAGS='--static'
export PATH=/cross_tools/x86_64-linux-musl-native/bin:$PATH
./configure --prefix=/
make
cp ./make /bin
