FROM busybox
ENV TARGET1=
ENV TARGET2=
ENV TARGET3=
ENTRYPOINT /bin/sh -c "export PATH=/d/bin:$PATH; upm makefile --production | upm make $TARGET1 $TARGET2 $TARGET3"
