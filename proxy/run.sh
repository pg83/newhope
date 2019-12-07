#!/bin/sh

docker run -ti -P -v "$(pwd)"/data:/root/.devpi "$@"
