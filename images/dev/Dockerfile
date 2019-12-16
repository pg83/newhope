FROM alpine:latest
COPY repositories /etc/apk/repositories
RUN apk update && apk upgrade && apk add clang gcc mc bash dash emacs xz-dev python3 lld llvm strace git 
ENTRYPOINT /bin/bash
