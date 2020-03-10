#!/bin/sh

set -e

cleanup() {
    rm -rf 1 || true
}

trap "cleanup" EXIT

rm -rf 1 >& /dev/null && mkdir 1 && cd 1
cli pkg init
cd ..
docker build .
