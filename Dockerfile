FROM antonsamokhvalov/newhope:latest
RUN rm /distro/runtime/*
COPY *.py /distro/runtime/
#RUN (apk add make bash curl wget tar xz python2 mc) && (cd /distro && mkdir workdir private managed)
ENV TARGET1=
ENV TARGET2=
ENV TARGET3=
ENTRYPOINT /bin/bash -c "cd /distro/runtime && /usr/bin/python2 ./main.py prefix=/distro plugins=/distro/plugins > Makefile && cat Makefile && make -j 1 Makefile $TARGET1 $TARGET2 $TARGET3"
