#!/bin/sh

exec docker run -ti --mount type=bind,src=/,dst=/srv $@ /pkg/yash-run-lmx8-v567bdf817cb7-pg/bin/yash -l --rcfile /etc/profile
