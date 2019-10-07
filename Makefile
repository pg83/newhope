SHELL=/bin/bash

ver = v1

xxm = $(ver)_x86_64-x86_64-musl-
xam = $(ver)_x86_64-aarch64-musl-
aam = $(ver)_aarch64-aarch64-musl-

txz = .tar.xz

fetch = cd `helper`; consume

LDFLAGS="--static"

$(xxm)init$(txz):
	$(fetch); mkdir $(xxm)init; cd $(xxm)init; \
	    wget https://www.busybox.net/downloads/binaries/1.31.0-defconfig-multiarch-musl/busybox-x86_64; \
	    mv busybox-x86_64 busybox; \
	    chmod +x busybox; \
	    produce $(xxm)init$(txz)

$(xxm)gcc$(txz): $(xxm)init$(txz)
	$(fetch) $(xxm)init$(txz); mkdir $(xxm)gcc; cd $(xxm)gcc; \
	    fetch_file https://musl.cc/x86_64-linux-musl-native.tgz; \
	    produce $(xxm)gcc$(txz)

$(xam)gcc$(txz): $(xxm)init$(txz)
	$(fetch) $(xxm)init$(txz); mkdir $(xam)gcc; cd $(xam)gcc; \
	    fetch_file https://musl.cc/aarch64-linux-musl-cross.tgz; \
	    produce $(xam)gcc$(txz)

$(aam)busybox$(txz): $(xxm)gcc$(txz) $(xam)gcc$(txz) $(xxm)init$(txz)
	$(fetch) $(xxm)gcc$(txz) $(xam)gcc$(txz) $(xxm)init$(txz); mkdir $(aam)busybox; cd $(aam)busybox; \
	    fetch_file https://busybox.net/downloads/busybox-1.31.0.tar.bz2; \
	    produce $(aam)busybox$(txz)
	    	
all: $(xxm)gcc$(txz) $(xam)gcc$(txz) $(xxm)init$(txz) $(aam)busybox$(txz)
