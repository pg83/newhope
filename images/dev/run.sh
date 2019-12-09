#!/bin/sh

exec docker run -ti --mount type=bind,src=$HOME,dst=/root 4aa2c1e9fc80
