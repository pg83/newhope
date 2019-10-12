FROM antonsamokhvalov/newhope:latest
ARG prefix=/distro
ARG target=all
COPY *.py ${prefix}/runtime/
RUN export PATH=/usr/bin:/usr/sbin:/bin:/sbin; (rm -rf /repo || true); apk add make bash curl && cd ${prefix}/runtime && /usr/bin/python2 ./main.py prune && /usr/bin/python2 ./main.py prefix=${prefix} > Makefile && make -j 1 Makefile ${target} && (cd ${prefix} && rm -rf managed private runtime workdir)
