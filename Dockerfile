FROM antonsamokhvalov/newhope:latest
COPY upm/upm /bin/
ENV TARGET1=
ENV TARGET2=
ENV TARGET3=
ENTRYPOINT /bin/bash -c "(cd /distro && rm -rf workdir managed private runtime >& /dev/null) || true; upm makefile --prefix /distro --plugins /distro/plugins > /distro/Makefile && upm make -f /distro/Makefile $TARGET1 $TARGET2 $TARGET3"
