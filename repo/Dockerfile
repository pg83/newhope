FROM antonsamokhvalov/newhope:latest
COPY *.py /runtime/
RUN apk add fdupes && cd / && mkdir /workdir /repo && cd /runtime && /usr/bin/python2 ./main.py && rm -rf /workdir /runtime
