#!/bin/sh

exec docker run -ti --mount type=bind,src=/,dst=/srv $@ /pkg/yash-lmx8-v5fc4af980df8-pg/bin/yash
