FROM alpine:latest
COPY repositories /etc/apk/repositories
RUN apk update && apk upgrade && apk add bash mc
COPY syncthing /bin/syncthing
EXPOSE 8384
EXPOSE 36687
ENTRYPOINT cd /root && while true; do (/bin/syncthing >& ./log); done
