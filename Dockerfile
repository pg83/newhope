FROM antonsamokhvalov/newhope:latest
COPY *.py /runtime/
RUN cd / && (mkdir /workdir || true) && (mkdir /repo || true) && cd /runtime && /usr/bin/python2 ./main.py && rm -rf /workdir /runtime /managed
