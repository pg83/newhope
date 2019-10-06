FROM newhope:latest
COPY Makefile /build/
COPY bootstrap_make.sh /build/
RUN cd /build; /bin/sh bootstrap_make.sh; rm -rf /build

