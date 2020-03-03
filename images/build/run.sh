#!/bin/sh

docker volume create build-build
docker volume create build-storage

exec docker run -ti -v build-build:/media/build -v build-storage:/media/storage $@
