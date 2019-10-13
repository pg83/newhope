FROM antonsamokhvalov/newhope:latest
RUN rm /distro/runtime/*
COPY upm /distro/runtime/upm
COPY cli /distro/runtime/
#RUN (apk add make bash curl wget tar xz python2 mc) && (cd /distro && mkdir workdir private managed)
ENV TARGET1=
ENV TARGET2=
ENV TARGET3=
ENTRYPOINT /bin/bash -c "cd /distro/runtime && /usr/bin/python2 cli makefile --prefix /distro --plugins /distro/plugins -b > /distro/Makefile && make -j1 -f /distro/Makefile $TARGET1 $TARGET2 $TARGET3"
