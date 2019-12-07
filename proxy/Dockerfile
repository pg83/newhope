FROM alpine:latest
RUN apk add python3 gcc python3-dev libc-dev libffi-dev && pip3 install --upgrade pip && pip3 install devpi-server && devpi-init
#ENTRYPOINT devpi-server
CMD ifconfig && (devpi-init || true) && devpi-server --host=172.17.0.2
EXPOSE 3141/tcp
