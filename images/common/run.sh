#!/bin/sh

exec docker run -ti --mount type=bind,src=/,dst=/srv $@ /pkg/yash-run-lmx8-v57dbfc354d0f-pg/bin/yash -l --rcfile /etc/profile
