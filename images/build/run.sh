#!/bin/sh

docker volume create build-root
docker volume create build-build
docker volume create build-storage

exec docker run -ti --net=host -v build-root:/root -v build-build:/media/build -v build-storage:/media/storage $@
