#!/bin/sh

set -e

trap "rm -rf ./1 >& /dev/null" exit

mkdir 1
cd 1
cli pkg init
cli pkg add @tini @small

cd ..

docker build .
