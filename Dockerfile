FROM antonsamokhvalov/newhope:latest
COPY *.py /runtime/
RUN cd / && mkdir /workdir && cd /runtime && /usr/bin/python2 ./main.py
# && rm -rf /workdir /runtime
