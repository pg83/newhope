FROM alpine:latest
COPY repositories /etc/apk/repositories
COPY upm /bin/upm
RUN apk update && apk upgrade && apk add clang dash bash mc python3 lld llvm git && ln -s /usr/bin/env /bin/
EXPOSE 10000
ENTRYPOINT exec /bin/bash -c 'while true; do (upm cmd scheduler BUILD >& /media/build/log) || true; done'
