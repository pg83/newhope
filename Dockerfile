FROM antonsamokhvalov/newhope:latest
ARG PKG=aarch64-musl-version.tar.gz
COPY Dockerfile Makefile.common Makefile.cross Makefile.host *.sh /runtime/
COPY gcc /cross_tools/x86_64-linux-musl-native/bin/
RUN cd /; mkdir /host; mkdir /cross; cd /host; make -j 4 -f /runtime/Makefile.host all; /cd /cross; make -j 4 -f /runtime/Makefile.cross ${PKG}; mv /cross/${PKG} /packages; rm -rf /host /runtime /cross
