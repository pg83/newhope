#!/bin/sh

set -e

(rm upm || true) 2> /dev/null
python3 ../../cli release > upm && chmod +x ./upm && python3 ./upm
docker build .
rm upm
