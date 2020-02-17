#!/bin/sh

set -e

trap "rm -rf 1 >& /dev/null" exit

rm -rf 1 >& /dev/null && mkdir 1 && cd 1
cli pkg init
cd ..
docker build .
rm -rf 1 >& /dev/null
