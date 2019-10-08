FROM antonsamokhvalov/newhope:latest
COPY *.py /runtime/
RUN cd /runtime && /usr/bin/python2 ./main.py prune && cd / && (mkdir /workdir || true) && (mkdir /repo || true) && cd /runtime && /usr/bin/python2 ./main.py && rm -rf /workdir /runtime /managed /private
