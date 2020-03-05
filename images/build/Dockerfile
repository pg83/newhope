FROM alpine:latest
COPY repositories /etc/apk/repositories
RUN apk update && apk upgrade && apk add clang dash bash mc python3 lld llvm git runit && ln -s /usr/bin/env /bin/
COPY upm /bin/upm
EXPOSE 10000
ENTRYPOINT cd /media && mkdir runit && cd runit && /bin/upm cmd scheduler --runit DOCKER >& /media/build/log
