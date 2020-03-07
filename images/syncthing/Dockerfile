FROM alpine:latest
COPY repositories /etc/apk/repositories
RUN apk update && apk upgrade && apk add bash mc
COPY syncthing /bin/syncthing
EXPOSE 10000
ENTRYPOINT cd /root && /bin/syncthing >& ./log
