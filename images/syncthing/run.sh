#!/bin/sh

docker volume create ss-root

exec docker run -ti --net=host -v ss-root:/root $@
