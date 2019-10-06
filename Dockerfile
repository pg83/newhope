FROM antonsamokhvalov/newhope:latest
ARG PKG
COPY Dockerfile Makefile.common Makefile.cross Makefile.host *.sh /runtime/
RUN cd /; mkdir /packages; mkdir /host; mkdir cross; cd /host; make -j 4 -f /runtime/Makefile.host; /cd /cross; make -j 4 -f /runtime/Makefile.cross ${PKG}; mv /cross/${PKG} /packages/; rm -rf /host /runtime /cross
