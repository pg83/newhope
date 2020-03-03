FROM alpine:latest
COPY repositories /etc/apk/repositories
COPY upm /bin/upm
RUN apk update && apk upgrade && apk add clang dash python3 lld llvm git && ln -s /usr/bin/env /bin/
EXPOSE 10000
ENTRYPOINT /bin/upm cmd scheduler BUILD
