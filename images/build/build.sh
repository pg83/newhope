#!/bin/sh

set -e

(rm upm || true) 2> /dev/null
cli release > upm && chmod +x ./upm && ./upm
docker build .
rm upm
