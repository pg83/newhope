#!/bin/sh

set -e

V="1.3.4"
F="syncthing-linux-amd64-v$V"
P="$F.tar.gz"

cleanup() {
    rm -rf "$F" "$P" syncthing || true
}

trap "cleanup" EXIT

curl -O -L "https://github.com/syncthing/syncthing/releases/download/v$V/$P"
tar -xf "$P"
mv "$F/syncthing" ./
docker build .
