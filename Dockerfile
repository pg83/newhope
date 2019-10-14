FROM antonsamokhvalov/newhope:latest
COPY upm/upm /bin/
ENV TARGET1=
ENV TARGET2=
ENV TARGET3=
ENTRYPOINT /bin/bash -c "(cd / && rm -rf workdir managed private runtime >& /dev/null) || true; (cd /d && rm -rf i w m p >& /dev/null) || true; upm makefile --prefix /d --install-dir /private > /tmp/Makefile && upm make -f /tmp/Makefile $TARGET1 $TARGET2 $TARGET3"
