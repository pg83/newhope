SHELL=/bin/bash

xxm = x86_64-x86_64-musl-
xam = x86_64-aarch64-musl-
aam = aarch64-aarch64-musl-
txz = .tar.xz

#rconsume = d = $(shell date | md5sum | base64) && cd /workdir && mkdir $(shell d) && cd $d && consume

$(xxm)init$(txz):
	cd `helper`; consume; pwd; mkdir $(xxm)init; cd $(xxm)init; \
	    fetch_file https://www.busybox.net/downloads/binaries/1.31.0-defconfig-multiarch-musl/busybox-x86_64; \
	    mv busybox-x86_64 busybox; \
	    chmod +x busybox; \
	    echo > rules; \
	    produce $(xxm)init$(txz)
	ls -la /repo/

$(xxm)gcc$(txz): $(xxm)init$(txz)
	cd `helper`; consume $(xxm)init$(txz); pwd; mkdir $(xxm)gcc; cd $(xxm)gcc; \
	    fetch_file https://musl.cc/x86_64-linux-musl-native.tgz; \
	    echo 'export PATH=bin/:$$PATH' > rules; \
	    produce $(xxm)gcc$(txz)
	ls -la /repo
	
all: $(xxm)gcc$(txz) $(xxm)init$(txz)
