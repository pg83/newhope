#!/bin/sh

pp=$(pwd)

set -e

trap "rm -rf $(pp)/1 >& /dev/null" exit

rm -rd 1 >& /dev/null
mkdir 1
cd 1
cli pkg init
cli pkg add @tini @small

cd ..

docker build .
