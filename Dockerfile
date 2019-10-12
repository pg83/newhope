FROM antonsamokhvalov/newhope:latest
RUN rm /distro/runtime/*
COPY *.py /distro/runtime/
#RUN (apk add make bash curl wget tar xz python2 mc) && (cd /distro && mkdir workdir private managed)
ENV TARGET=love
ENTRYPOINT /bin/bash -c "ln -sf /repo/packages /distro/repo && cd /distro/runtime && /usr/bin/python2 ./main.py prefix=/distro plugins=/repo/plugins > Makefile && make -j 1 Makefile $TARGET"
