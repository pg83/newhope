#!/bin/sh

exec docker run -ti --mount type=bind,src=$HOME,dst=/root $@

